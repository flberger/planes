help:
	@echo Targets: docs, clean, user_install, sdist

docs: clean
	/home/florian/temp/python/pydoctor/bin/pydoctor --verbose \
	                                                --add-package clickndrag \
	                                                --make-html \
                                                    --html-output doc/

clean:
	rm -fv *.pyc
	rm -fv */*.pyc

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
