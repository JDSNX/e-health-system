# <center style="color:orange">💵 **API PARA SA THESIS SA ECE** 💵</center>


# /get
- returns all users information

```python
{
    "result": {
        "K8IQ1": {
            "first_name": "Test",
            "last_name": "Man",
            "middle_initial": "T",
            "password": "madafapaka",
            "ref_id": "K8IQ1",
            "result": {
                "BLOOD_OXYGEN_LEVEL": "ASDFGH",
                "BODY_TEMPERATURE": "1234",
                "ECG_RESULT": "ASDFG,"
            },
            "timestamp": 1648962733.597915
        },
        "NC4H0": {
            "first_name": "Z18RK7F3C1",
            "last_name": "2ELTKFJHEW",
            "middle_initial": "8",
            "password": "r3db3rr13s",
            "ref_id": "NC4H0",
            "result": {
                "BLOOD_OXYGEN_LEVEL": "ASDFGH",
                "BODY_TEMPERATURE": 265,
                "ECG_RESULT": "ASDFG,"
            },
            "timestamp": 1648963013.316237
        }
    },
    "success": true,
    "timestamp": 1649253394.396461
}
```

# /get_user
- return specific user

**Parameters:**
    - `ref_id` - id of the user 

```python
{
    "result": {
        "K8IQ1": {
            "first_name": "Test",
            "last_name": "Man",
            "middle_initial": "T",
            "password": "madafapaka",
            "ref_id": "K8IQ1",
            "result": {
                "BLOOD_OXYGEN_LEVEL": "ASDFGH",
                "BODY_TEMPERATURE": "1234",
                "ECG_RESULT": "ASDFG,"
            },
            "timestamp": 1648962733.597915
        },
    },
    "success": true,
    "timestamp": 1649253394.396461
}
```

# /update_pass
- return specific user

**Parameters:**
    - `ref_id` - id of the user 
    - `password` - new password

```python
{
    "result": "OK"
    "success": true,
    "timestamp": 1649253394.396461
}
```

# /delete
- delete specific user

**Parameters:**
    - `ref_id` - id of the user 

```python
{
    "result": "OK"
    "success": true,
    "timestamp": 1649253394.396461
}
```
