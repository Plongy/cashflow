# Cashflow 2.0

Django project to manage receipts and reimbursements at Datasektionen.

## Setup

Install the packages in `requirements.txt`. You can then run the django-server with `manage.py runserver`.
Make sure you first set up a database, an S3 bucket and supply the correct environment variables as specified below.


TODO: Make sure the packages are up to date/throw out old stuff

## Run

The following environment variables are required to run the project:

| Variable              | Description                           | Default                       |
|-----------------------|---------------------------------------|-------------------------------|
| DB_HOST               | PostgreSQL server hostname            | localhost                     |
| DB_NAME               | PostgreSQL database                   | cashflow                      |
| DB_USER               | PostgreSQL username                   | postgres                      |
| DB_PASS               | PostgreSQL password                   | postgres                      |
| DB_PORT               | PostgreSQL port                       | 5432                          |
| DEBUG                 | Django debug mode                     | False                         |
| SECRET_KEY            | Django encryption key                 | ---                           |
| LOGIN2_KEY            | Login2 API key for KTH authentication | ---                           |
| S3_BUCKET_NAME        | Amazon AWS s3 bucket name             | ---                           |
| S3_ACCESS_KEY_ID      | Amazon AWS IAM access key id          | ---                           |
| S3_SECRET_ACCESS_KEY  | Amazon AWS IAM secret access key      | ---                           |
| S3_USE_SIGV4          | If Frankfurt, set to False            | True                          |
| S3_HOST               | Url to s3 server                      | s3.eu-central-1.amazonaws.com |
| SPAM_API_KEY          | API key for the spam mail system      | ---                           |


## API documentation

### Creating a new expense
Method: `PUT`<br>
URL: `/api/expense/new/`

**Request:**
json:
```
{

}
```

### Updating expense
Method: `PUT`<br>
URL: `/api/expense/<id>/`


### Getting expense by id
Method: `GET`<br>
URL: `/api/expense/<id>/`

Get a `expense` by its `id`, also retrieves `expense_parts` and `budget_lines` associated with the expense.

<br>

**Response:**
```
{
   "expense":{
      "owner_first_name":"John",
      "reimbursement":null,
      "description":"Foo",
      "owner_last_name":"Doe",
      "expense_date":"2017-03-05",
      "verification":"E231",
      "expense_parts":[
         {
            "budget_line":{
               "budget_line_name":"mat",
               "cost_centre":{
                  "cost_centre_name":"dwrek",
                  "committee":{
                     "committee_name":"Drek",
                     "committee_id":1
                  },
                  "cost_centre_id":2
               },
               "budget_line_id":3
            },
            "attest_date":"2017-03-06",
            "amount":12,
            "attested_by":"foba",
            "id":5
         }
      ],
      "owner":2,
      "id":1,
      "owner_username":"johdo"
   }
}
```


### Getting all expenses
Method: `GET`<br>
URL: `/api/expense/`

Retrieves all expenses current user is elegible to view

**Responese:**
```
{
    "expenses": [<List of expenses>]
}
```

### Getting all expenses belonging to user
Method: `GET`<br>
URL: `/api/user/<username>/expenses/`

Retrieves all expenses belonging to the user with the specified `kthid`/`username`.

**Responese:**
```
{
    "expenses": [<List of expenses>]
}
```


### Get all unattested expenses

Method: `GET`<br>
URL: `/api/attest/`

Retrieves all the expenses that the current user can attest that haven't been attested yet.

**Responese:**
```
{"expenses": [<List of expenses>]
```

### Attest expenses
Method: `POST`<br>
URL: `/api/attest/`

Attest all the specified reciepts

**Request:**
list:
```
[1,22,23,12]
```

**Response:**
```
{
  'success': true
}
```

### Get current user
Method: `GET`<br>
URL: `/api/user/`

Get the currently logged in

**Response:**
```
{
   "user":{
      "username":"foba",
      "bank_name":"Swedbank",
      "first_name":"Foo",
      "last_name":"Bar",
      "sorting_number":"2322-1",
      "default_account":{
         "id":1,
         "name":"DKM"
      },
      "bank_account":"2131231231"
   }
}
```

### Get user
Method: `GET`<br>
URL: `/api/user/<username>/`

Get a user by its `kthid`/`username`

**Response:**
```
{
   "user":{
      "username":"foba",
      "bank_name":"Swedbank",
      "first_name":"Foo",
      "last_name":"Bar",
      "sorting_number":"2322-1",
      "default_account":{
         "id":1,
         "name":"DKM"
      },
      "bank_account":"2131231231"
   }
}
```

### Get budget
Method: `GET`<br>
URL: `/api/budget/`


**Response:**
```
{
   "committees":[
      {
         "committee_name":"D-rektoratet",
         "committee_id":1,
         "cost_centres":[
            {
               "cost_centre_name":"Allmänt",
               "cost_centre_id":1,
               "budget_lines":[
                  {
                     "budget_line_name":"MUTA",
                     "budget_line_id":1
                  },
                  {
                     "budget_line_name":"Representation",
                     "budget_line_id":2
                  }
               ]
            }
         ]
      }
   ]
}
```
