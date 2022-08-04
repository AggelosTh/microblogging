# Microblogging project
This project is based on FastAPI and uses alembic for database migrations.
Our current DB modeling allows multiple users where each user can have multiple blogs (although the API assumes one blog per user).
Each blog can have multiple articles.
# Installation instructions
You can start using this repo by executing the following command:
```bash
docker-compose up -d
```
Then you can inspect the API via the Swagger Interface at http://localhost:8000/docs/.

# Endpoints description
All requested endpoints have been implemented.

## User and Blog management
1. New users can be created via the following endpoint: POST(api/v1/users)
2. All the users can be listed here: GET(api/v1/users)
3. A blog instance is created automatically whenever a user is created

## Blog articles
1. Blog articles can be created via: POST(api/v1/blogs)
2. Can be edited via: PUT(api/v1/blogs/{id})

## Tags
Tags can be specified as a list of strings whenever a blog article is created.
They can also be overriden when an article is edited, by specifying a new list of tags.
If no list of tags is provided when an article is updated, then they remain unchanged.

## Article publication
When an article is created it is automatically considered to be in a draft-state.
There is an endpoint for publishing a specific article that also takes an optional
timestamp for the publication date.
If no timestamp is specified then the article is marked as "published" with a publication date of the current time. Otherwise
it is marked as "pre-published" and an external job should mark it as "published" at the specified date (which is currently stored in the db as well).

The relevant endpoint is the following: POST(api/v1/blogs/publish/{id})

## Article body
The article body is expected to be in a markdown format and it is 
automatically rendered as HTML via the API.

## Search tag
Searching by tag is supported by two endpoints:
1. Globally across all blogs at: GET(api/v1/blogs/blog/search)
2. Inside a single user: GET(api/v1/blogs/blog/{user_id}/search)
