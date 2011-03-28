help:
	@echo Targets:
	@echo '    docs'
	@echo '    clean'
	@echo '    pylint'
	@echo '    errors'
	@echo '    user_install'
	@echo '    sdist'

docs: clean
	/home/florian/temp/python/pydoctor/bin/pydoctor --verbose \
	                                                --add-package clickndrag \
	                                                --make-html \
                                                    --html-output doc/

clean:
	rm -fv *.pyc
	rm -fv */*.pyc

pylint:
	pylint clickndrag ; pylint examples/clickndrag_interactive.py

errors:
	pylint --errors-only clickndrag ; pylint --errors-only examples/clickndrag_interactive.py

ifdef PYTHON

user_install:
	$(PYTHON) setup.py install --user --record user_install-filelist.txt

sdist:
	$(PYTHON) setup.py sdist --force-manifest --formats=bztar,zip

else

user_install:
	@echo Please supply Python executable as PYTHON=executable.

sdist:
	@echo Please supply Python executable as PYTHON=executable.

endif

