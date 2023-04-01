from fastapi import FastAPI, status, Response
from typing import Optional
from pydantic import BaseModel
import sqlite3

app = FastAPI()

con = sqlite3.connect("todo.db", check_same_thread=False)
db = con.cursor()

class TodoItem(BaseModel):
    title: str 
    description: Optional[str] = None
    completed: Optional[bool] = False

class UpdateItem(BaseModel):
    title: Optional[str] 
    description: Optional[str] = None
    completed: Optional[bool] = False


@app.get("/", status_code=status.HTTP_200_OK)
async def list():
    db.execute("SELECT * FROM todo")

    todo_items = []

    for row in db.fetchall():
        item = {"id": row[0], "title": row[1], "description": row[2], "completed": row[3]}
        todo_items.append(item)

    return todo_items


@app.post("/", status_code=status.HTTP_201_CREATED)
async def add(item: TodoItem):
    
    db.execute("INSERT INTO todo (title, description, completed) VALUES (?, ?, ?)", 
               (item.title, item.description, item.completed))
    con.commit()
    
    return {"status": "item added succesfully"}


@app.put("/edit/{id}", status_code=status.HTTP_200_OK)
async def edit(id: int, item: UpdateItem):

    db.execute("SELECT id FROM todo")
    base = [i[0] for i in db.fetchall()]

    if id not in base:
        Response.status_code=status.HTTP_204_NO_CONTENT
        return {"Error": "Item ID doesn't exists"}
    
    if item.title is not None:
        db.execute("UPDATE todo SET title = ? WHERE id = ?",
                   (item.title, id))
        con.commit()
        
    if item.description is not None:
        db.execute("UPDATE todo SET description = ? WHERE id = ?",
                   (item.description, id))
        con.commit()

    if item.completed is not None:
        db.execute("UPDATE todo SET completed = ? WHERE id = ?", 
                   (item.completed, id))
        con.commit()

    return {"id": id, "title": item.title, "description": item.description, "completed": item.completed}


@app.delete("/delete/{id}", status_code=status.HTTP_200_OK)
async def delete(id: int):

    db.execute("SELECT id FROM todo")
    base = [i[0] for i in db.fetchall()]

    if id not in base:
        Response.status_code=status.HTTP_204_NO_CONTENT
        return {"Error": "Item ID doesn't exists"}
    
    db.execute("DELETE FROM todo WHERE id = ?", 
               (id,))
    con.commit()

    return {"status": "item deleted succesfully"}

    

