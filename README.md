# AlarmButton

This is repository for the backend and frontend admin page for the project.


### new apk file

Any new version of the smartphone APK should be added as `redbutton.apk` to 
`local-static` folder.



### collect static
```commandline

python manage.py collectstatic --no-input
```

## with the new database 

### migrate
```commandline
python manage.py migrate
```

### load data from fixtures
 ```commandline
 manage.py loaddata alarmbutton/fixtures/fixtures.json
 ```



