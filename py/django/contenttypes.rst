django.contrib.contenttypes.models.ContentType
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- The Admin application uses it to log the history of each object added or
  changed the admin interface.
- Django's authencation framework uses it to tie user permissions to
  specific models
- Django's comments system (django.contrib.comments) uses it "attach"
  comments to any installed model

contentType: 存储model的信息，可以通过 app_label, model_name 还原
