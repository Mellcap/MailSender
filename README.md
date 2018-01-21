# MailSender
MailSender is a service that automatically sends email.

In order to have a better experience, I build an **[Online Demo](http://www.wenziyu.me:5000/)**. I highly encourage you to try it.


## OverView

### Installation
1. Install Docker
2. Clone this repo
	```bash
	git clone https://github.com/Mellcap/MailSender.git
	```

3. Edit `docker-compose.yml`, set your email configuration
4. Run
	```bash
	docker-compose up -d
	```
5. Running on `http://0.0.0.0:5000/`


### Details

#### Structures
```
├── app
│   ├── __init__.py		 ===>   Application factory
│   ├── api                             --------------------
│   │   ├── __init__.py
│   │   ├── email_events.py	 ===>   API handle requests
│   │   ├── email_groups.py
│   │   └── errors.py                   --------------------
│   ├── email.py		 ===>   Send email (celery)
│   ├── exceptions.py		 ===>   Handle exceptions
│   ├── form				-------------------
│   │   ├── __init__.py
│   │   ├── email_events.py	 ===>   Forms
│   │   └── email_groups.py		-------------------
│   ├── models
│   │   ├── __init__.py
│   │   ├── email_event.py
│   │   ├── email_event_form.py	  ===>   Models
│   │   ├── email_group.py
│   │   ├── email_group_form.py          -------------------
│   ├── schedules.py              ===>   Celery Schedules
│   ├── templates 			 -------------------
│   │   ├── base.html
│   │   ├── email_events.html
│   │   ├── email_groups.html     ===>   Templates
│   │   ├── home.html
│   │   ├── save_email_groups.html
│   │   └── save_emails.html             -------------------
│   ├── utils.py                  ===>   Utils
├── celeryconfig.py		  ===>   Celery Schedule Config
├── config.py			  ===>   App config(Served for many environments)
├── docker-compose.yml
├── manage.py			  ===>   Manage file
├── migrations				 -------------------
│   ├── README
│   ├── alembic.ini
│   ├── env.py			  ===>   Database Migration
│   ├── script.py.mako
│   └── versions
│       ├── f2512412c77a_.py		 -------------------
├── requirements.txt
├── setup.py
├── tests				 -------------------
│   ├── __init__.py
│   ├── test_basics.py
│   ├── test_save_email.py	  ===>   Unittests
│   ├── test_send_email.py
│   ├── utils.py			 -------------------
└── wait-for-it.sh		  ===>   A script that let server wait database setup
```

It is worth to say that the `create_app` function at MailSender/app/__init__/py is an application factory, which takes config_name as an argument the name of a configuration to use for the application.

#### Models
There are three models.

* `Email Group` & `Email Address`, the relation of them is **many-to many**.
	* The reason why I build `Email Group` is to reduce the work of the stuff, or he/she will input all the emails every time.
	* Because an email address can belong to many email groups, so I set the relation of them is many-to-many.
	* When saving data, it will validate all the fields.
		* group_name: type & length & repeat
		* email_address: type & length & format & repeat
		* You can see the details at: MailSender/app/models/email_group.py
* `Email Event` is the model which can save emails and send it automatically in the future.
	* When saving data, it will validate all the fields.
		* event_id: type
		* email_group_id: type & exist
		* email_subject: type & length
		* email_content: type
		* timestamp: make sure timestamp > now
		* repeat: avoid send same email to the same group
		* You can see the details at: MailSender/app/models/email_event.py

#### APIs
##### @api
* /save_emails: save email data into db.
	* Method: POST
	* @param: event_id int
    * @param: email_group_id int
    * @param: email_subject str
    * @param: email_content str
    * @param: timestamp str
    * @param: timezone str notRequired default=Asia/Singapore 
* /email_groups: create new email_group.
	* Method: POST
	* @param: group_name str unique
* /email_groups/<int:email_group_id>/email_addresses: create new email_address in a certain email_group
	* Method: POST
    * @param: email_group_id int
    * @param: email_addresses str // if many, divided by comma
* /email_addresses: create new email_address
	* Method: POST
	* @param: group_name str unique

##### @form
* /forms/save_emails: save email data into db.
* /forms/get_emails: get email data from db.
* /forms/save_email_groups: save email group into db.
* /forms/get_email_groups: get email group from db.


#### Schedules
Use Celery and Redis to enhance the performance.

* Celery Beat: to do periodic tasks, check email events every minute.
	* Config: you can see the config file at MailSender/celeryconfig.py

#### Tests
Test all the features of `save email` and `send email`

