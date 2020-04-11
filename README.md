# instacart
Check delivery times for stores


# install
clone this repo then install python requirements (preferably in a virtualenv), and also sendmail and mutt.

```
$ pip install -r requirements.txt
$ sudo apt install mutt
$ sudo apt install sendmail
```

# create .env file

rename the sample.env file to .env and fill in with your username, password and an email to get notified at


# usage

```
>>> import instacart
>>>
>>> ins = instacart.Instacart()
>>>
>>> ins.check_delivery_times(ins.STORES["COSTCO"])

Delivery Arrives Today - Apr 16
Delivery Thu, Apr 16, 2pm - 4pm
Delivery Thu, Apr 16, 3pm - 5pm
Delivery Thu, Apr 16, 5pm - 7pm
Delivery Fri, Apr 24, 11am - 1pm
Delivery Fri, Apr 24, 12pm - 2pm
Delivery Fri, Apr 24, 1pm - 3pm
Delivery Fri, Apr 24, 2pm - 4pm
Delivery Fri, Apr 24, 3pm - 5pm
Delivery Fri, Apr 24, 4pm - 6pm
Delivery Fri, Apr 24, 5pm - 7pm
Delivery Fri, Apr 24, 6pm - 8pm
```
