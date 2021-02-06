Changelog
=========

1.1.0 (2021-02-06)
------------------

* 58bece6_ - Migration for change to ``SavedReport.run_by``
* fae699c_ - Full code base format + commit of change to ``SavedReport.run_by``.
  Modified to add the ``on_delete=models.SET_NULL``

.. _58bece6: https://github.com/gadventures/django-reports-admin/commit/58bece6
.. _fae699c: https://github.com/gadventures/django-reports-admin/commit/fae699c

1.0.4 (2017-02-28)
------------------

* a0dc5a0_ - Return ``None`` on error when calling ``ModelReport``

.. _a0dc5a0: https://github.com/gadventures/django-reports-admin/commit/a0dc5a0

1.0.3 (2017-02-27)
------------------

* 21ca6a5_ - Refactor calling to report runner
* fba6bf1_ - Allow queryset to be passed within __init__ method
* 5f0ef05_ - Add simple test case for ModelReport, refine misc.
* 3d7d587_ - Document shell usage in README, add more type hints
* 5268739_ - Adjust signature of run_report, easing usage in shell

.. _21ca6a5: https://github.com/gadventures/django-reports-admin/commit/21ca6a5
.. _fba6bf1: https://github.com/gadventures/django-reports-admin/commit/fba6bf1
.. _5f0ef05: https://github.com/gadventures/django-reports-admin/commit/5f0ef05
.. _3d7d587: https://github.com/gadventures/django-reports-admin/commit/3d7d587
.. _5268739: https://github.com/gadventures/django-reports-admin/commit/5268739

1.0.2 (2017-02-10)
------------------

* fa46174_ Adjust user messaging in admin.
* Update README

.. _fa46174: https://github.com/gadventures/django-reports-admin/commit/fa46174

1.0.1 (2017-02-10)
------------------

* First pypi release

1.0.0 (2017-02-09)
------------------

* Initial commit
