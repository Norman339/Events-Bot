#!/usr/bin/env python3
"""
Database Test Script for CyberBot
This script demonstrates how to test the database functionality
"""

import asyncio
import sys
import os
from pathlib import Path
from dotenv import load_dotenv

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Ensure environment variables from .env are loaded BEFORE importing db
load_dotenv()
from bot.utils.database import db

async def test_database():
    """Test all database functions"""
    print("🚀 Starting Database Test...")
    print("=" * 50)
    
    # Connectivity check: ping MongoDB first
    try:
        await db.client.admin.command('ping')
        print("✅ Connected to MongoDB (ping successful)")
    except Exception as e:
        print("❌ Could not connect to MongoDB. Check MONGODB_URI and network.")
        print(f"Error: {e}")
        return
    
    # Test 1: Check current storage method
    print(f"📊 Storage Method: {'MongoDB' if db.use_mongodb else 'JSON Files'}")
    
    # Test 2: Test events functionality
    print("\n📅 Testing Events...")
    
    # Clear existing events (start fresh)
    await db.clear_events()
    print("✅ Cleared existing events")
    
    # Add test events
    test_events = [
        {
            'title': 'Cybersecurity Workshop',
            'date': '2024-12-15',
            'description': 'Learn about ethical hacking and penetration testing',
            'created_by': 123456789,
            'created_at': '2024-12-01T10:00:00'
        },
        {
            'title': 'CTF Competition',
            'date': '2024-12-20',
            'description': 'Annual Capture The Flag competition',
            'created_by': 123456789,
            'created_at': '2024-12-01T11:00:00'
        }
    ]
    
    for event in test_events:
        await db.add_event(event)
        print(f"✅ Added event: {event['title']}")
    
    # Retrieve events
    events = await db.get_events()
    print(f"📋 Retrieved {len(events)} events:")
    for i, event in enumerate(events, 1):
        print(f"  {i}. {event['title']} - {event['date']}")
    
    # Test modifying an event
    print("\n✏️ Testing Event Modification...")
    updated = await db.modify_event(
        'Cybersecurity Workshop',
        new_description='Updated: Learn advanced ethical hacking techniques'
    )
    if updated:
        print("✅ Successfully modified event")
        print(f"   New description: {updated['description']}")
    
    # Test removing an event
    print("\n🗑️ Testing Event Removal...")
    removed = await db.remove_event('CTF Competition')
    if removed:
        print("✅ Successfully removed CTF Competition event")
    
    # Final event count
    final_events = await db.get_events()
    print(f"📊 Final event count: {len(final_events)}")
    
    # Test 3: Test facts functionality
    print("\n🔒 Testing Cybersecurity Facts...")
    
    # Get random fact
    fact = await db.get_random_fact()
    if fact:
        print(f"✅ Random fact: {fact}")
    else:
        print("⚠️ No facts available")
    
    # Test adding a new fact
    new_fact = "Test fact: Always use strong passwords with at least 12 characters!"
    await db.add_fact(new_fact)
    print(f"✅ Added new fact: {new_fact}")
    
    # Get another random fact
    fact2 = await db.get_random_fact()
    if fact2:
        print(f"✅ Another random fact: {fact2}")
    
    print("\n" + "=" * 50)
    print("✅ Database test completed successfully!")
    print(f"📁 Data stored in: {'MongoDB' if db.use_mongodb else 'JSON files in ./data/'}")

if __name__ == "__main__":
    # Create data directory if it doesn't exist
    Path("data").mkdir(exist_ok=True)
    
    # Run the test
    asyncio.run(test_database())