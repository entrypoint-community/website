# Database Schema: `Entrypoint-DB`

## Table: `community_members`

| Column Name | Data Type    | Constraints            | Description                                       |
|-------------|--------------|------------------------|---------------------------------------------------|
| id          | SERIAL       | PRIMARY KEY            | Auto-incrementing integer that serves as the primary key for the table. |
| name        | VARCHAR(255) | NOT NULL               | Name of the community member. This is a mandatory field. |
| email       | VARCHAR(255) | NOT NULL, UNIQUE       | Email address of the community member. This is a mandatory field and must be unique. |
| phone       | VARCHAR(20)  | NOT NULL, UNIQUE       | Phone number of the community member |

## SQL for table creation

```sql
CREATE TABLE community_members (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    phone VARCHAR(20) NOT NULL UNIQUE
);
