#!/usr/bin/env python3
"""
Todo Manager
============
A simple, persistent command-line todo list manager.

Features:
- Add, list, complete, and delete tasks
- Persistent storage (saves to todo.json)
- Priority levels
- Due dates (optional)
- Interactive mode perfect for Pydroid

Author: RetroMatt2077
"""

import argparse
import json
import os
from datetime import datetime
from pathlib import Path


TODO_FILE = "todo.json"


def load_todos():
    """Load todos from JSON file."""
    if os.path.exists(TODO_FILE):
        try:
            with open(TODO_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return []
    return []


def save_todos(todos):
    """Save todos to JSON file."""
    with open(TODO_FILE, 'w', encoding='utf-8') as f:
        json.dump(todos, f, indent=2)


def add_task(title, priority="medium", due=None):
    todos = load_todos()
    task = {
        "id": len(todos) + 1,
        "title": title,
        "completed": False,
        "priority": priority.lower(),
        "due": due,
        "created": datetime.now().strftime("%Y-%m-%d %H:%M")
    }
    todos.append(task)
    save_todos(todos)
    print(f"✅ Task added: {title}")


def list_tasks(show_all=False):
    todos = load_todos()
    if not todos:
        print("📭 No tasks yet. Add one with --add")
        return

    print(f"\n📋 Todo List ({len(todos)} tasks)\n")
    for task in todos:
        if not show_all and task["completed"]:
            continue
            
        status = "✅" if task["completed"] else "⬜"
        priority = task["priority"].upper()[:1]
        due = f" (due: {task['due']})" if task.get("due") else ""
        
        print(f"{status} {task['id']:2d}. [{priority}] {task['title']}{due}")


def complete_task(task_id):
    todos = load_todos()
    for task in todos:
        if task["id"] == task_id:
            task["completed"] = True
            save_todos(todos)
            print(f"✅ Task #{task_id} marked as complete!")
            return
    print(f"❌ Task #{task_id} not found.")


def delete_task(task_id):
    todos = load_todos()
    original_length = len(todos)
    todos = [t for t in todos if t["id"] != task_id]
    
    if len(todos) < original_length:
        save_todos(todos)
        print(f"🗑️  Task #{task_id} deleted.")
    else:
        print(f"❌ Task #{task_id} not found.")


def main():
    parser = argparse.ArgumentParser(description="✅ Todo Manager")
    parser.add_argument("-a", "--add", type=str, help="Add a new task")
    parser.add_argument("-l", "--list", action="store_true", help="List all tasks")
    parser.add_argument("-c", "--complete", type=int, help="Mark task as complete by ID")
    parser.add_argument("-d", "--delete", type=int, help="Delete task by ID")
    parser.add_argument("-p", "--priority", choices=["low", "medium", "high"], default="medium")
    parser.add_argument("--due", help="Due date (YYYY-MM-DD)")
    parser.add_argument("--all", action="store_true", help="Show completed tasks too")
    parser.add_argument("--prompt", action="store_true", help="Interactive mode")

    args = parser.parse_args()

    if args.prompt or not any([args.add, args.list, args.complete, args.delete]):
        print("📋 Todo Manager - Interactive Mode\n")
        print("1. Add task")
        print("2. List tasks")
        print("3. Complete task")
        print("4. Delete task")
        print("5. Exit")
        
        while True:
            choice = input("\nChoose an option (1-5): ").strip()
            if choice == "1":
                title = input("Task title: ").strip()
                if title:
                    priority = input("Priority (low/medium/high): ").strip().lower() or "medium"
                    due = input("Due date (YYYY-MM-DD, optional): ").strip() or None
                    add_task(title, priority, due)
            elif choice == "2":
                list_tasks(show_all=True)
            elif choice == "3":
                try:
                    tid = int(input("Task ID to complete: "))
                    complete_task(tid)
                except:
                    print("Invalid ID")
            elif choice == "4":
                try:
                    tid = int(input("Task ID to delete: "))
                    delete_task(tid)
                except:
                    print("Invalid ID")
            elif choice == "5":
                print("👋 Goodbye!")
                break
            else:
                print("Invalid option")
    else:
        if args.add:
            add_task(args.add, args.priority, args.due)
        if args.list or args.all:
            list_tasks(show_all=args.all)
        if args.complete:
            complete_task(args.complete)
        if args.delete:
            delete_task(args.delete)


if __name__ == "__main__":
    main()
