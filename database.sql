CREATE TABLE todo(
    id INTEGER PRIMARY KEY, 
    title TEXT NOT NULL, 
    description TEXT NOT NULL, 
    completed INTEGER NOT NULL DEFAULT 0 CHECK (completed IN (0,1)));