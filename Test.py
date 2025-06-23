import pytest
import os
import json
from unittest.mock import patch
from db import create_db, find_matching_patterns
from Parse_console_args import Parse_console_args
from DataType import DataType
import main

# Test DataType.py
class TestDataType:
    def test_email_validation(self):
        dt = DataType("test@example.com")
        assert dt.type == "email"
        
    def test_phone_validation(self):
        dt = DataType("+7 123 456 78 90")
        assert dt.type == "phone"
        
    def test_date_validation_dot_format(self):
        dt = DataType("01.01.2023")
        assert dt.type == "date"
        
    def test_date_validation_dash_format(self):
        dt = DataType("2023-01-01")
        assert dt.type == "date"
        
    def test_text_validation(self):
        dt = DataType("some random text")
        assert dt.type == "text"

# Test Parse_console_args.py
class TestParseConsoleArgs:
    def test_single_arg_parsing(self):
        with patch('sys.argv', ['script.py', '--name=Test']):
            result = Parse_console_args()
            assert result == {'name': 'Test'}
            
    def test_multiple_args_parsing(self):
        with patch('sys.argv', ['script.py', '--name=Test', '--email=test@test.com']):
            result = Parse_console_args()
            assert result == {'name': 'Test', 'email': 'test@test.com'}
            
    def test_duplicate_args_error(self):
        with patch('sys.argv', ['script.py', '--name=Test', '--name=Test2']), \
             pytest.raises(Exception, match="Два аргумента с одним именем"):
            Parse_console_args()

# Test db.py
class TestDB:
    @pytest.fixture(autouse=True)
    def setup_and_teardown(self):
        # Setup
        if os.path.exists("db/db.json"):
            os.remove("db/db.json")
        os.makedirs("db", exist_ok=True)
        create_db()
        yield
        # Teardown
        if os.path.exists("db/db.json"):
            os.remove("db/db.json")
    
    def test_create_db(self):
        assert os.path.exists("db/db.json")
        with open("db/db.json") as f:
            data = json.load(f)
            assert len(data['_default']) == 3
            
    def test_find_matching_patterns_full_match(self):
        pattern = {"username": "text", "email": "email"}
        results = find_matching_patterns(pattern)
        assert len(results) == 1
        assert results[0]['name'] == 'Test1'
        
    def test_find_matching_patterns_partial_match(self):
        pattern = {"username": "text"}
        results = find_matching_patterns(pattern)
        assert len(results) == 3
        
    def test_find_matching_patterns_no_match(self):
        pattern = {"nonexistent": "value"}
        results = find_matching_patterns(pattern)
        assert len(results) == 0
        
    def test_find_matching_patterns_empty_pattern(self):
        pattern = {}
        results = find_matching_patterns(pattern)
        assert len(results) == 3

# Test main.py
class TestMain:
    @patch('main.Parse_console_args')
    @patch('main.find_matching_patterns')
    def test_main_with_match(self, mock_find, mock_parse):
        mock_parse.return_value = {'username': 'text', 'email': 'email'}
        mock_find.return_value = [{'name': 'Test1'}]
        
        with patch('builtins.print') as mock_print:
            main.main()
            mock_print.assert_called_with('Test1')
            
    @patch('main.Parse_console_args')
    @patch('main.find_matching_patterns')
    def test_main_without_match(self, mock_find, mock_parse):
        mock_parse.return_value = {'nonexistent': 'value'}
        mock_find.return_value = []
        
        with patch('builtins.print') as mock_print:
            main.main()
            mock_print.assert_called_with({'nonexistent': 'text'})  # 'text' is default type

            
    @patch('sys.argv', ['main.py'])  # Пустые аргументы
    @patch('main.find_matching_patterns')
    @patch('main.create_db')
    def test_main_db_creation(self, mock_create, mock_find):
        mock_find.return_value = []
        main.main()
        mock_create.assert_called_once()
        

# Integration test
class TestIntegration:
    @patch('main.Parse_console_args')
    @patch('main.find_matching_patterns')
    def test_end_to_end_flow(self, mock_find, mock_parse):
        test_args = {'username': 'text', 'email': 'test@test.com'}
        mock_parse.return_value = test_args
        mock_find.return_value = [{'name': 'Test1'}]
        
        with patch('builtins.print') as mock_print:
            main.main()
            mock_print.assert_called_with('Test1')
            
            expected_pattern = {
                'username': 'text',
                'email': 'email'
            }
            mock_find.assert_called_with(expected_pattern)
