-- Migration to add source_url column to articles table
-- Run this in your Supabase SQL editor

-- Add source_url column to existing articles table
ALTER TABLE articles ADD COLUMN IF NOT EXISTS source_url VARCHAR(500);

-- Update existing articles to have a default source_url
UPDATE articles SET source_url = 'Legacy import' WHERE source_url IS NULL; 