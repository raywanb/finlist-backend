-- Enable the pgvector extension
CREATE EXTENSION IF NOT EXISTS vector;

-- Create the articles table
CREATE TABLE articles (
    id SERIAL PRIMARY KEY,
    author VARCHAR(255) NOT NULL,
    title VARCHAR(500) NOT NULL,
    content TEXT NOT NULL,
    date TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    category VARCHAR(100) NOT NULL,
    source_url VARCHAR(500), -- URL source of the article
    embeddings VECTOR(1536) -- Using 1536 dimensions for OpenAI text-embedding-ada-002 model
);

-- Create the users table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    articles INTEGER[] DEFAULT '{}' -- Array of article IDs
);

-- Create indexes for better performance
CREATE INDEX idx_articles_category ON articles(category);
CREATE INDEX idx_articles_date ON articles(date);
CREATE INDEX idx_articles_author ON articles(author);
CREATE INDEX idx_users_email ON users(email);

-- Create an HNSW index for the embeddings vector (for semantic search)
-- HNSW is generally recommended for pgvector as it provides good performance
-- for both build time and query time
CREATE INDEX ON articles USING hnsw (embeddings vector_cosine_ops);

-- Alternative: IVFFlat index (comment out HNSW above if using this)
-- CREATE INDEX ON articles USING ivfflat (embeddings vector_cosine_ops) WITH (lists = 100);

-- Create a function for semantic search using pgvector
CREATE OR REPLACE FUNCTION match_articles(
    query_embedding VECTOR(1536),
    match_threshold FLOAT DEFAULT 0.78,
    match_count INT DEFAULT 10
)
RETURNS TABLE (
    id INT,
    author VARCHAR(255),
    title VARCHAR(500),
    content TEXT,
    date TIMESTAMP WITH TIME ZONE,
    category VARCHAR(100),
    similarity FLOAT
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT
        articles.id,
        articles.author,
        articles.title,
        articles.content,
        articles.date,
        articles.category,
        1 - (articles.embeddings <=> query_embedding) AS similarity
    FROM articles
    WHERE 1 - (articles.embeddings <=> query_embedding) > match_threshold
    ORDER BY articles.embeddings <=> query_embedding
    LIMIT match_count;
END;
$$;

-- Create a function for hybrid search (semantic + category filtering)
CREATE OR REPLACE FUNCTION hybrid_search_articles(
    query_embedding VECTOR(1536),
    category_filter VARCHAR(100) DEFAULT NULL,
    match_threshold FLOAT DEFAULT 0.78,
    match_count INT DEFAULT 10
)
RETURNS TABLE (
    id INT,
    author VARCHAR(255),
    title VARCHAR(500),
    content TEXT,
    date TIMESTAMP WITH TIME ZONE,
    category VARCHAR(100),
    similarity FLOAT
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT
        articles.id,
        articles.author,
        articles.title,
        articles.content,
        articles.date,
        articles.category,
        1 - (articles.embeddings <=> query_embedding) AS similarity
    FROM articles
    WHERE 1 - (articles.embeddings <=> query_embedding) > match_threshold
        AND (category_filter IS NULL OR articles.category = category_filter)
    ORDER BY articles.embeddings <=> query_embedding
    LIMIT match_count;
END;
$$;

-- Enable Row Level Security (RLS) for better security
ALTER TABLE articles ENABLE ROW LEVEL SECURITY;
ALTER TABLE users ENABLE ROW LEVEL SECURITY;

-- Create policies for articles (allow public read access, authenticated write access)
CREATE POLICY "Articles are viewable by everyone" ON articles
    FOR SELECT USING (true);

CREATE POLICY "Articles can be created by authenticated users" ON articles
    FOR INSERT WITH CHECK (true);

-- Create policies for users (basic structure for future authentication)
CREATE POLICY "Users can view their own data" ON users
    FOR SELECT USING (true);

CREATE POLICY "Users can create accounts" ON users
    FOR INSERT WITH CHECK (true);

-- Create a function to update the articles array in users table
CREATE OR REPLACE FUNCTION update_user_articles()
RETURNS TRIGGER AS $$
BEGIN
    -- Add article ID to user's articles array when article is created
    IF TG_OP = 'INSERT' THEN
        UPDATE users 
        SET articles = array_append(articles, NEW.id)
        WHERE id = (SELECT id FROM users WHERE name = NEW.author LIMIT 1);
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Create trigger to automatically update user's articles array
CREATE TRIGGER trigger_update_user_articles
    AFTER INSERT ON articles
    FOR EACH ROW
    EXECUTE FUNCTION update_user_articles();

-- Insert some sample data for testing
INSERT INTO articles (author, title, content, category) VALUES
('John Doe', 'Tesla Stock Analysis: Q4 2023 Review', 'Tesla has shown remarkable growth in Q4 2023 with strong delivery numbers and expanding market share in the EV sector. The company continues to innovate with new models and technology improvements.', 'Technology'),
('Jane Smith', 'Market Trends: AI Stocks in 2024', 'Artificial Intelligence stocks are expected to continue their upward trajectory in 2024. Companies like NVIDIA, Microsoft, and Alphabet are leading the charge in AI innovation.', 'Technology'),
('Mike Johnson', 'Oil Prices and Energy Sector Outlook', 'Recent geopolitical events have impacted oil prices significantly. Energy companies are adapting to new market conditions and renewable energy transitions.', 'Energy'),
('Sarah Wilson', 'Cryptocurrency Market Analysis', 'Bitcoin and other cryptocurrencies are showing signs of recovery. Institutional adoption and regulatory clarity are key factors driving market sentiment.', 'Cryptocurrency');

-- Insert sample users
INSERT INTO users (name, email, password) VALUES
('John Doe', 'john.doe@example.com', 'hashed_password_here'),
('Jane Smith', 'jane.smith@example.com', 'hashed_password_here'),
('Mike Johnson', 'mike.johnson@example.com', 'hashed_password_here'),
('Sarah Wilson', 'sarah.wilson@example.com', 'hashed_password_here');