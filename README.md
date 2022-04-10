Django Leave Request programming test task
==========================================

Introduction
------------

This application uses `Python 3` and Django `2.2.x`. It contains a `leave` module for managing employee leave requests. 

Your job is to finish an implementation of the it's functionality using CBV and i18n.


Task details
------------

There are multiple test placed in the project that will help you ascertain a subset things that need to be implemented,
but bear in mind that there are more test that are not visible to you and they will test everything else that is needed.   

We have placed a TODO comments in the code to help you track requirements, here are examples:

- Add user admin for models.User
- Make sure text translations remain in place
- Show language and manager in list table columns
- Use leave.models.User as a User model replacement for authentications
- Use 'user' and 'users' as display texts in Admin
- Make request timestamp set automatically
- Fill in all the user visible field and model names and descriptions
- Make sure request wont be deleted by changes to the user table contents
- Limit access to authenticated users
- Turn on pagination of 20 items per page
- Setup user foreign keys from request
- Setup success redirect to LeaveRequestDetail
- Allow manager to review this request by POST submit value of status=accepted/rejected
- Validate submit value is in ('accepted', 'rejected') return HttpResponseBadRequest
- return HttpResponseForbidden if non manager tries to POST
- Redirect anonymous users to login
- On successful update redirect to LeaveRequestDetail
- Raise PermissionDenied for Users other than `LeaveRequest.request_by`
- Make sure empty values won't show as "None"
- Instead of Status number show it's name


Please note how TODOs are verified
----------------------------------

Be sure to complete all TODOs, but know not everything is explicitly tested.

The tests that are visible to you are not the only ones, some TODO tasks does not have a matching test inside 
your project but they will be tested upon submission and these test results will be visible only to the person scoring your solution. 

The best approach would be to leave TODO comments until all tests that you see pass. 
Then you should review and compare TODOs with your changes and look for TODOs that are yet to be completed.  


Environment setup
-----------------

This test is better solved in the IDE that you are familiar with, please clone the task.

To execute all unit tests, use:

    pip install -q -e . && python3 setup.py pytest
