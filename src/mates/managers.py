from django.db import models


class MateGameInfoManager(models.Manager):
    def create(self, user_id, **kwargs):
        mategameinfo = self.model(
            user_id=user_id,
            **kwargs,
        )

        mategameinfo.full_clean()
        mategameinfo.save()

        return mategameinfo
