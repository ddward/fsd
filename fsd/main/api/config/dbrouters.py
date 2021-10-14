from api.models import AnnualFullFormatted


class FinDataRouter:
    """Route API models to the fin_data database
       Router reference: 
       https://docs.djangoproject.com/en/3.2/topics/db/multi-db/
    """
    route_app_labels = {'api'}

    def db_for_read(self, model, **hints):
        if model._meta.app_label in self.route_app_labels:
            return 'fin_db'
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label in self.route_app_labels:
            return 'fin_db'
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        print(app_label)
        print(model_name)
        if app_label in self.route_app_labels:
            return db == "fin_db"
        return None