from django.db import models

model_str = 'some_app.some_model'
mod = models.get_model(*model_str.split('.'))
objects = mod._default_manager.all()
