# Basic Tests for the application
import pytest
import json
from flask import url_for


class TestApp:

    def test_ping(self, client):
        """Test server responds"""
        res = client.get(url_for("ping"))
        assert res.status_code == 200
        assert res.json == {"ping": "pong"}

    def test_hawkeye_contentful(self, contentful_client):
        """Test Hawkeye is a charcter in the content"""
        post = contentful_client.entry("2SiSYthyVaasy84IssCQAw")
        assert post.title == "Hawkeye"
        assert post.slug == "hawkeye"
        assert post.first_appearance == "Tales of Suspense #57 (Sept. 1964)"
        assert post.gif is not None

    def test_content_type_post(self, contentful_client):
        """Test content model of a post"""
        post_content_type = contentful_client.content_type("post")
    # Expect 5 fields in a post now that we’ve added an author field.
        assert len(post_content_type.fields) == 5
        title = next(d for d in post_content_type.fields if d.id == "title")
        assert title.id == "title"
        assert title.type == "Symbol"
        author = next(d for d in post_content_type.fields if d.id == "author")
        assert author.id == "author"
        assert author.type == "Symbol"

    def test_hawkeye_get(self, client):
        """Test Hawkeye is listed as a charcter on the index route"""
        res = client.get(url_for("index"))
        assert b"Hawkeye" in res.data
