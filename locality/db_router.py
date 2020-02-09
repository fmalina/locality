ROUTE_DB = 'geo'
ROUTE_APPS = ['locality', 'geonames']
ROUTE_REL = ROUTE_APPS + ['listing']


class DbRouter(object):
    """
    Determine how to route database calls for Medd models.
    All other models will be routed to the next router in the DATABASE_ROUTERS
    setting if applicable, or otherwise to the default database.

        DATABASE_ROUTERS = ['{ this app }.db_router.DbRouter']
    """

    def db_for_read(self, model, instance=None, **hints):
        """Send all read operations on routed app models to routed database.

        MySQL does support cross database foreign keys on the same DB server on InnoDB
        http://www.youdidwhatwithtsql.com/cross-database-foreign-keys/784/
        Django doesn't
        https://docs.djangoproject.com/en/3.0/topics/db/multi-db/#cross-database-relations
        """
        if model._meta.app_label in ROUTE_APPS:
            return ROUTE_DB
        return None

    def db_for_write(self, model, **hints):
        """Send all write operations on routed app models to routed database."""
        if model._meta.app_label in ROUTE_APPS:
            return ROUTE_DB
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """Determine if relationship is allowed between two objects."""
        # Allow any relation between two models that are both in the routed app.
        if obj1._meta.app_label in ROUTE_REL and obj2._meta.app_label in ROUTE_REL:
            return True
        # No opinion if neither object is in the routed app (defer to default or other routers).
        elif all([x not in [obj1._meta.app_label, obj2._meta.app_label] for x in ROUTE_REL]):
            return None

        # Block relationship if one object is in the routed app and the other isn't.
            return False

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """Ensure that the routed app's models get created on the right database."""
        if app_label in ROUTE_APPS:
            # Medd app should be migrated only on the routed database.
            return db == ROUTE_DB
        elif db == ROUTE_DB:
            # Ensure that all other apps don't get migrated on the routed database.
            return False

        # No opinion for all other scenarios
        return None
