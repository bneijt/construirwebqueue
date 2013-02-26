Construir web queue
===================

Status: Public development. Running this code at https://construir-bneijt.rhcloud.com/

Introduction
============
Construir is a simple "run this job tar inside a KVM". This
web application is intended to be a public Openshift
application to test the sharing of jobs in a public queue.

Within the construir project a "web fetching job runner" will
be created, which can then download public jobs from this web queue
and upload done jobs.

Done jobs are jobs that match `d[0-9]+.tar.xz`, new jobs are `i[0-9]+.tar.xz`.

Both can be uploaded using the HTTP form. Done jobs get an url (which may be polled) and only a random job can be downloaded.

