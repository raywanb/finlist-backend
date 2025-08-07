import requests
import json
import time
from typing import Dict, Any, List

class StockAnalysisAPITester:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.session = requests.Session()
        self.test_results = []
        
    def log_test(self, test_name: str, status: str, details: str = ""):
        """Log test results"""
        result = {
            "test": test_name,
            "status": status,
            "details": details,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        self.test_results.append(result)
        print(f"[{status.upper()}] {test_name}: {details}")
        
    def test_root_endpoint(self) -> bool:
        """Test the root endpoint"""
        try:
            response = self.session.get(f"{self.base_url}/")
            if response.status_code == 200:
                data = response.json()
                if "message" in data and "version" in data:
                    self.log_test("Root Endpoint", "PASS", f"Response: {data['message']}")
                    return True
                else:
                    self.log_test("Root Endpoint", "FAIL", "Missing expected fields")
                    return False
            else:
                self.log_test("Root Endpoint", "FAIL", f"Status code: {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Root Endpoint", "ERROR", f"Exception: {str(e)}")
            return False
    
    def test_health_check(self) -> bool:
        """Test the health check endpoint"""
        try:
            response = self.session.get(f"{self.base_url}/health")
            if response.status_code == 200:
                data = response.json()
                if data.get("status") == "healthy":
                    self.log_test("Health Check", "PASS", "Service is healthy")
                    return True
                else:
                    self.log_test("Health Check", "FAIL", f"Unexpected status: {data}")
                    return False
            else:
                self.log_test("Health Check", "FAIL", f"Status code: {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Health Check", "ERROR", f"Exception: {str(e)}")
            return False
    
    def test_get_all_articles(self) -> bool:
        """Test getting all articles"""
        try:
            response = self.session.get(f"{self.base_url}/api/v1/articles/")
            if response.status_code == 200:
                articles = response.json()
                if isinstance(articles, list):
                    self.log_test("Get All Articles", "PASS", f"Retrieved {len(articles)} articles")
                    return True
                else:
                    self.log_test("Get All Articles", "FAIL", "Response is not a list")
                    return False
            else:
                self.log_test("Get All Articles", "FAIL", f"Status code: {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Get All Articles", "ERROR", f"Exception: {str(e)}")
            return False
    
    def test_get_article_by_id(self) -> bool:
        """Test getting a specific article by ID"""
        try:
            response = self.session.get(f"{self.base_url}/api/v1/articles/1")
            if response.status_code == 200:
                article = response.json()
                if "id" in article and "title" in article:
                    self.log_test("Get Article by ID", "PASS", f"Retrieved article: {article['title']}")
                    return True
                else:
                    self.log_test("Get Article by ID", "FAIL", "Missing required fields")
                    return False
            else:
                self.log_test("Get Article by ID", "FAIL", f"Status code: {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Get Article by ID", "ERROR", f"Exception: {str(e)}")
            return False
    
    def test_get_article_by_title(self) -> bool:
        """Test getting a specific article by title"""
        try:
            # First get an article to know its title
            response = self.session.get(f"{self.base_url}/api/v1/articles/1")
            if response.status_code == 200:
                article = response.json()
                title = article['title']
                
                # Now test getting by title
                encoded_title = title.replace(' ', '%20')  # URL encode spaces
                response = self.session.get(f"{self.base_url}/api/v1/articles/title/{encoded_title}")
                if response.status_code == 200:
                    found_article = response.json()
                    if found_article['title'] == title:
                        self.log_test("Get Article by Title", "PASS", f"Retrieved article: {title}")
                        return True
                    else:
                        self.log_test("Get Article by Title", "FAIL", "Title mismatch")
                        return False
                else:
                    self.log_test("Get Article by Title", "FAIL", f"Status code: {response.status_code}")
                    return False
            else:
                self.log_test("Get Article by Title", "FAIL", "Could not get reference article")
                return False
        except Exception as e:
            self.log_test("Get Article by Title", "ERROR", f"Exception: {str(e)}")
            return False
    
    def test_search_articles_by_title(self) -> bool:
        """Test searching articles by title (partial match)"""
        try:
            # Search for articles with "Tesla" in the title
            response = self.session.get(f"{self.base_url}/api/v1/articles/search-title/Tesla")
            if response.status_code == 200:
                articles = response.json()
                if isinstance(articles, list) and len(articles) > 0:
                    # Check if any article contains "Tesla" in the title
                    tesla_articles = [a for a in articles if 'Tesla' in a['title']]
                    if tesla_articles:
                        self.log_test("Search Articles by Title", "PASS", f"Found {len(articles)} articles with 'Tesla' in title")
                        return True
                    else:
                        self.log_test("Search Articles by Title", "FAIL", "No articles found with 'Tesla' in title")
                        return False
                else:
                    self.log_test("Search Articles by Title", "FAIL", "No articles found")
                    return False
            else:
                self.log_test("Search Articles by Title", "FAIL", f"Status code: {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Search Articles by Title", "ERROR", f"Exception: {str(e)}")
            return False
    
    def test_create_article(self) -> bool:
        """Test creating a new article"""
        try:
            article_data = {
                "title": "Test Article: API Testing",
                "content": "This is a test article created during API testing to verify the create endpoint functionality.",
                "category": "Technology",
                "author": "API Tester"
            }
            
            response = self.session.post(
                f"{self.base_url}/api/v1/articles/",
                json=article_data,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                article = response.json()
                if "id" in article and article["title"] == article_data["title"]:
                    self.log_test("Create Article", "PASS", f"Created article with ID: {article['id']}")
                    return True
                else:
                    self.log_test("Create Article", "FAIL", "Article not created properly")
                    return False
            else:
                self.log_test("Create Article", "FAIL", f"Status code: {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Create Article", "ERROR", f"Exception: {str(e)}")
            return False
    
    def test_semantic_search(self) -> bool:
        """Test semantic search functionality"""
        try:
            search_data = {
                "query": "smartphone market",
                "limit": 3
            }
            
            response = self.session.post(
                f"{self.base_url}/api/v1/articles/search",
                json=search_data,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                results = response.json()
                if isinstance(results, list):
                    self.log_test("Semantic Search", "PASS", f"Found {len(results)} relevant articles")
                    return True
                else:
                    self.log_test("Semantic Search", "FAIL", "Response is not a list")
                    return False
            else:
                self.log_test("Semantic Search", "FAIL", f"Status code: {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Semantic Search", "ERROR", f"Exception: {str(e)}")
            return False
    
    def test_hybrid_search(self) -> bool:
        """Test hybrid search functionality"""
        try:
            search_data = {
                "query": "technology companies",
                "limit": 3
            }
            
            response = self.session.post(
                f"{self.base_url}/api/v1/articles/hybrid-search?category=Technology",
                json=search_data,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                results = response.json()
                if isinstance(results, list):
                    # Verify all results are in Technology category
                    all_tech = all(article.get("category") == "Technology" for article in results)
                    if all_tech:
                        self.log_test("Hybrid Search", "PASS", f"Found {len(results)} technology articles")
                        return True
                    else:
                        self.log_test("Hybrid Search", "FAIL", "Not all results are in Technology category")
                        return False
                else:
                    self.log_test("Hybrid Search", "FAIL", "Response is not a list")
                    return False
            else:
                self.log_test("Hybrid Search", "FAIL", f"Status code: {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Hybrid Search", "ERROR", f"Exception: {str(e)}")
            return False
    
    def test_get_articles_by_category(self) -> bool:
        """Test getting articles by category"""
        try:
            response = self.session.get(f"{self.base_url}/api/v1/articles/category/Technology")
            if response.status_code == 200:
                articles = response.json()
                if isinstance(articles, list):
                    # Verify all articles are in Technology category
                    all_tech = all(article.get("category") == "Technology" for article in articles)
                    if all_tech:
                        self.log_test("Get Articles by Category", "PASS", f"Found {len(articles)} technology articles")
                        return True
                    else:
                        self.log_test("Get Articles by Category", "FAIL", "Not all articles are in Technology category")
                        return False
                else:
                    self.log_test("Get Articles by Category", "FAIL", "Response is not a list")
                    return False
            else:
                self.log_test("Get Articles by Category", "FAIL", f"Status code: {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Get Articles by Category", "ERROR", f"Exception: {str(e)}")
            return False
    
    def test_get_categories(self) -> bool:
        """Test getting all categories"""
        try:
            response = self.session.get(f"{self.base_url}/api/v1/categories/")
            if response.status_code == 200:
                categories = response.json()
                if isinstance(categories, list) and len(categories) > 0:
                    self.log_test("Get Categories", "PASS", f"Found categories: {', '.join(categories)}")
                    return True
                else:
                    self.log_test("Get Categories", "FAIL", "No categories found or invalid response")
                    return False
            else:
                self.log_test("Get Categories", "FAIL", f"Status code: {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Get Categories", "ERROR", f"Exception: {str(e)}")
            return False
    
    def test_error_handling(self) -> bool:
        """Test error handling for non-existent resources"""
        try:
            # Test non-existent article
            response = self.session.get(f"{self.base_url}/api/v1/articles/999")
            if response.status_code == 404:
                data = response.json()
                if "detail" in data and "not found" in data["detail"].lower():
                    self.log_test("Error Handling", "PASS", "Proper 404 response for non-existent article")
                    return True
                else:
                    self.log_test("Error Handling", "FAIL", "Unexpected error response format")
                    return False
            else:
                self.log_test("Error Handling", "FAIL", f"Expected 404, got {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Error Handling", "ERROR", f"Exception: {str(e)}")
            return False
    
    def test_response_format(self) -> bool:
        """Test that responses are properly formatted JSON"""
        try:
            response = self.session.get(f"{self.base_url}/api/v1/articles/")
            if response.status_code == 200:
                # Check if response is valid JSON
                try:
                    data = response.json()
                    if isinstance(data, list):
                        self.log_test("Response Format", "PASS", "Valid JSON response with proper structure")
                        return True
                    else:
                        self.log_test("Response Format", "FAIL", "Response is not a list")
                        return False
                except json.JSONDecodeError:
                    self.log_test("Response Format", "FAIL", "Response is not valid JSON")
                    return False
            else:
                self.log_test("Response Format", "FAIL", f"Status code: {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Response Format", "ERROR", f"Exception: {str(e)}")
            return False
    
    def run_all_tests(self) -> Dict[str, Any]:
        """Run all tests and return summary"""
        print("🚀 Starting Stock Analysis API Tests...")
        print("=" * 50)
        
        tests = [
            ("Root Endpoint", self.test_root_endpoint),
            ("Health Check", self.test_health_check),
            ("Get All Articles", self.test_get_all_articles),
            ("Get Article by ID", self.test_get_article_by_id),
            ("Get Article by Title", self.test_get_article_by_title),
            ("Search Articles by Title", self.test_search_articles_by_title),
            ("Create Article", self.test_create_article),
            ("Semantic Search", self.test_semantic_search),
            ("Hybrid Search", self.test_hybrid_search),
            ("Get Articles by Category", self.test_get_articles_by_category),
            ("Get Categories", self.test_get_categories),
            ("Error Handling", self.test_error_handling),
            ("Response Format", self.test_response_format)
        ]
        
        passed = 0
        failed = 0
        errors = 0
        
        for test_name, test_func in tests:
            try:
                if test_func():
                    passed += 1
                else:
                    failed += 1
            except Exception as e:
                self.log_test(test_name, "ERROR", f"Test crashed: {str(e)}")
                errors += 1
        
        print("=" * 50)
        print("📊 Test Summary:")
        print(f"✅ Passed: {passed}")
        print(f"❌ Failed: {failed}")
        print(f"💥 Errors: {errors}")
        print(f"📈 Success Rate: {(passed / (passed + failed + errors) * 100):.1f}%")
        
        return {
            "summary": {
                "passed": passed,
                "failed": failed,
                "errors": errors,
                "total": passed + failed + errors,
                "success_rate": (passed / (passed + failed + errors) * 100) if (passed + failed + errors) > 0 else 0
            },
            "results": self.test_results
        }
    
    def save_results(self, filename: str = "test_results.json"):
        """Save test results to JSON file"""
        results = self.run_all_tests()
        with open(filename, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"💾 Test results saved to {filename}")
        return results

def main():
    """Main function to run the tests"""
    # Wait a moment for server to be ready
    print("⏳ Waiting for server to be ready...")
    time.sleep(2)
    
    # Create tester instance
    tester = StockAnalysisAPITester()
    
    # Run tests and save results
    results = tester.save_results()
    
    # Exit with appropriate code
    if results["summary"]["failed"] == 0 and results["summary"]["errors"] == 0:
        print("🎉 All tests passed!")
        exit(0)
    else:
        print("⚠️  Some tests failed!")
        exit(1)

if __name__ == "__main__":
    main() 