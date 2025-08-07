# Stock Analysis API Test Suite

This test suite provides comprehensive testing for the Stock Analysis API endpoints. It includes both automated tests and manual testing instructions.

## 📋 Test Coverage

The test suite covers the following endpoints and functionality:

### ✅ Core Endpoints
- **Root Endpoint** (`GET /`) - Welcome message and API info
- **Health Check** (`GET /health`) - Service health status
- **Get All Articles** (`GET /api/v1/articles/`) - Retrieve all articles
- **Get Article by ID** (`GET /api/v1/articles/{id}`) - Retrieve specific article
- **Create Article** (`POST /api/v1/articles/`) - Create new article with embeddings

### 🔍 Search Functionality
- **Semantic Search** (`POST /api/v1/articles/search`) - AI-powered semantic search
- **Hybrid Search** (`POST /api/v1/articles/hybrid-search`) - Combined semantic + category filtering
- **Category Filtering** (`GET /api/v1/articles/category/{category}`) - Filter by category
- **Get Categories** (`GET /api/v1/categories/`) - List all available categories

### 🛡️ Error Handling & Quality
- **Error Handling** - 404 responses for non-existent resources
- **Response Format** - Valid JSON responses with proper structure

## 🚀 Quick Start

### Prerequisites
1. Ensure the API server is running on `http://localhost:8000`
2. Install test dependencies:
   ```bash
   pip install -r test_requirements.txt
   ```

### Running Tests
```bash
python test_api.py
```

### Expected Output
```
⏳ Waiting for server to be ready...
🚀 Starting Stock Analysis API Tests...
==================================================
[PASS] Root Endpoint: Response: Welcome to Stock Analysis API
[PASS] Health Check: Service is healthy
[PASS] Get All Articles: Retrieved 10 articles
[PASS] Get Article by ID: Retrieved article: Tesla Stock Analysis: Q4 2023 Review
[PASS] Create Article: Created article with ID: 11
[PASS] Semantic Search: Found 3 relevant articles
[PASS] Hybrid Search: Found 3 technology articles
[PASS] Get Articles by Category: Found 9 technology articles
[PASS] Get Categories: Found categories: Technology, Cryptocurrency, Energy
[PASS] Error Handling: Proper 404 response for non-existent article
[PASS] Response Format: Valid JSON response with proper structure
==================================================
📊 Test Summary:
✅ Passed: 11
❌ Failed: 0
💥 Errors: 0
📈 Success Rate: 100.0%
💾 Test results saved to test_results.json
🎉 All tests passed!
```

## 📊 Test Results

The test suite generates detailed results in JSON format:

### Test Results File (`test_results.json`)
```json
{
  "summary": {
    "passed": 11,
    "failed": 0,
    "errors": 0,
    "total": 11,
    "success_rate": 100.0
  },
  "results": [
    {
      "test": "Root Endpoint",
      "status": "PASS",
      "details": "Response: Welcome to Stock Analysis API",
      "timestamp": "2025-08-07 11:54:34"
    }
    // ... more test results
  ]
}
```

## 🧪 Individual Test Details

### 1. Root Endpoint Test
- **Purpose**: Verify API is accessible and returns welcome message
- **Expected**: 200 status with message and version fields
- **Test Data**: None required

### 2. Health Check Test
- **Purpose**: Verify service health status
- **Expected**: 200 status with "healthy" status
- **Test Data**: None required

### 3. Get All Articles Test
- **Purpose**: Verify article retrieval functionality
- **Expected**: 200 status with list of articles
- **Test Data**: None required

### 4. Get Article by ID Test
- **Purpose**: Verify single article retrieval
- **Expected**: 200 status with article containing id and title
- **Test Data**: Uses article ID 1

### 5. Create Article Test
- **Purpose**: Verify article creation with automatic embedding generation
- **Expected**: 200 status with created article containing ID
- **Test Data**: Creates test article with Technology category

### 6. Semantic Search Test
- **Purpose**: Verify AI-powered semantic search functionality
- **Expected**: 200 status with relevant articles
- **Test Data**: Searches for "smartphone market"

### 7. Hybrid Search Test
- **Purpose**: Verify combined semantic + category filtering
- **Expected**: 200 status with technology articles only
- **Test Data**: Searches for "technology companies" in Technology category

### 8. Category Filtering Test
- **Purpose**: Verify category-based filtering
- **Expected**: 200 status with only Technology articles
- **Test Data**: Filters by Technology category

### 9. Get Categories Test
- **Purpose**: Verify category listing functionality
- **Expected**: 200 status with list of available categories
- **Test Data**: None required

### 10. Error Handling Test
- **Purpose**: Verify proper error responses
- **Expected**: 404 status for non-existent article
- **Test Data**: Requests article ID 999

### 11. Response Format Test
- **Purpose**: Verify JSON response structure
- **Expected**: Valid JSON with proper data types
- **Test Data**: None required

## 🔧 Customization

### Testing Different Endpoints
You can modify the test suite to test additional endpoints:

```python
def test_custom_endpoint(self) -> bool:
    """Test a custom endpoint"""
    try:
        response = self.session.get(f"{self.base_url}/api/v1/custom/")
        if response.status_code == 200:
            self.log_test("Custom Endpoint", "PASS", "Custom endpoint working")
            return True
        else:
            self.log_test("Custom Endpoint", "FAIL", f"Status code: {response.status_code}")
            return False
    except Exception as e:
        self.log_test("Custom Endpoint", "ERROR", f"Exception: {str(e)}")
        return False
```

### Testing Different Base URLs
```python
# Test against different server
tester = StockAnalysisAPITester("http://your-server:8000")
```

### Adding Custom Test Data
```python
# Modify test data in individual test methods
article_data = {
    "title": "Your Custom Title",
    "content": "Your custom content",
    "category": "Your Category",
    "author": "Your Author"
}
```

## 🐛 Troubleshooting

### Common Issues

1. **Server Not Running**
   ```
   [ERROR] Root Endpoint: Exception: Connection refused
   ```
   **Solution**: Start the API server with `python main.py`

2. **Port Already in Use**
   ```
   [ERROR] Root Endpoint: Exception: Address already in use
   ```
   **Solution**: Kill existing process or change port

3. **Missing Dependencies**
   ```
   ModuleNotFoundError: No module named 'requests'
   ```
   **Solution**: Install dependencies with `pip install -r test_requirements.txt`

4. **Database Connection Issues**
   ```
   [FAIL] Create Article: Status code: 500
   ```
   **Solution**: Check Supabase connection and environment variables

### Debug Mode
To see detailed HTTP requests, modify the test class:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 📈 Performance Testing

The test suite includes basic performance metrics:

- **Response Time**: Each test logs execution time
- **Success Rate**: Overall test success percentage
- **Error Tracking**: Detailed error logging

## 🔄 Continuous Integration

This test suite is designed for CI/CD integration:

```yaml
# Example GitHub Actions workflow
- name: Run API Tests
  run: |
    python test_api.py
  env:
    SUPABASE_URL: ${{ secrets.SUPABASE_URL }}
    SUPABASE_KEY: ${{ secrets.SUPABASE_KEY }}
    OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
```

## 📝 Manual Testing

For manual testing, you can use the provided curl commands:

```bash
# Test root endpoint
curl "http://localhost:8000/"

# Test health check
curl "http://localhost:8000/health"

# Test get all articles
curl "http://localhost:8000/api/v1/articles/"

# Test semantic search
curl -X POST "http://localhost:8000/api/v1/articles/search" \
  -H "Content-Type: application/json" \
  -d '{"query": "smartphone market", "limit": 3}'
```

## 🤝 Contributing

To add new tests:

1. Create a new test method in the `StockAnalysisAPITester` class
2. Add the test to the `tests` list in `run_all_tests()`
3. Update this README with test documentation
4. Ensure the test follows the existing pattern and error handling

## 📄 License

This test suite is part of the Stock Analysis API project. 