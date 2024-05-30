# Database Schema: `Entrypoint-DB`

## Table: `users`

| Column Name | Data Type    | Constraints            | Description                                       |
|-------------|--------------|------------------------|---------------------------------------------------|
| id          | SERIAL       | PRIMARY KEY            | Auto-incrementing integer that serves as the primary key for the table. |
| name        | VARCHAR(255) | NOT NULL               | Name of the user. This is a mandatory field. |
| role        | VARCHAR(255) | NOT NULL               | Role of the user. This is a mandatory field. |
| email       | VARCHAR(255) | NOT NULL, UNIQUE       | Email address of the user. This is a mandatory field and must be unique. |
| phone       | VARCHAR(20)  | NOT NULL, UNIQUE       | Phone number of the user. This is a mandatory field and must be unique. |

## Table: `blog_posting`

| Column Name     | Data Type  | Constraints            | Description                                       |
|-----------------|------------|------------------------|---------------------------------------------------|
| id              | SERIAL     | PRIMARY KEY            | Auto-incrementing integer that serves as the primary key for the table. |
| name            | VARCHAR(255)| NOT NULL              | Name of the blog post. This is a mandatory field. |
| role            | VARCHAR(255)| NOT NULL              | Role associated with the blog post. This is a mandatory field. |
| creation_date   | DATE       | NOT NULL               | Date when the blog post was created. This is a mandatory field. |
| description     | TEXT       |                        | Description of the blog post.                     |
| link            | VARCHAR(255)|                       | Link to the blog post.                            |

## SQL for Table Creation

### `users`

```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    role VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    phone VARCHAR(20) NOT NULL UNIQUE
);
```

### `blog_posting`
```sql
CREATE TABLE blog_posting (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    role VARCHAR(255) NOT NULL,
    creation_date DATE NOT NULL,
    description TEXT,
    link VARCHAR(255)
);
