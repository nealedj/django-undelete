from django.db import models


class TrashableQuerySet(models.query.QuerySet):
    """Special QuerySet that explicitly calls delete() method on each model.
    If we don't do this, QuerySet delete() will bypass our TrashableMixin
    delete().

    This is only used for the NonTrashedManager. TrashedManager returns
    trashed objects, which should be truly deleted when delete() is called.
    Logic is the same for TrashableMixin at second delete().

    @author: Charl P. Botha <cpbotha@timescapers.com>
    """

    def delete(self, trash=True):
        """Overrides normal QuerySet delete to call explicitly object's
        delete() method.
        """
        if trash:
            for m in self:
                m.delete()

        else:
            super(TrashableQuerySet, self).delete()


class BaseNonTrashedManager(models.Manager):
    ''' Query only objects which have not been trashed. '''
    def get_queryset(self):
        return super(BaseNonTrashedManager, self).get_queryset().filter(
            trashed_at__isnull=True)

NonTrashedManager = BaseNonTrashedManager.from_queryset(TrashableQuerySet)


class TrashedManager(models.Manager):
    ''' Query only objects which have been trashed. '''
    def get_queryset(self):
        query_set = super(TrashedManager, self).get_queryset()
        return query_set.filter(trashed_at__isnull=False)
