help:
	@echo Targets:
	@echo '    docs'
	@echo '    clean'
	@echo '    pylint'
	@echo '    errors'
	@echo '    user_install'
	@echo '    sdist'
	@echo '    commit.txt'
	@echo '    commit'
	@echo '    sign'
	@echo '    freshmeat'

docs: clean
	/home/florian/temp/python/pydoctor/bin/pydoctor --verbose \
	                                                --add-package planes \
	                                                --make-html \
                                                    --html-output doc/

clean:
	rm -vf `find . -iname '*.log'`
	rm -rvf `find . -type d -iname '__pycache__'`
	rm -vf `find . -iname '*.pyc'`

pylint:
	pylint planes ; pylint examples/planes_interactive.py

errors:
	pylint --errors-only planes ; pylint --errors-only examples/planes_interactive.py

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

commit.txt:
	# single line because bzr diff returns false when there are diffs
	#
	bzr diff > commit.txt ; nano commit.txt

commit:
	@echo RETURN to commit using commit.txt, CTRL-C to cancel:
	@read DUMMY
	bzr commit --file commit.txt && rm -v commit.txt

sign:
	rm -vf dist/*.asc
	for i in dist/*.*z* ; do gpg --sign --armor --detach $$i ; done
	gpg --verify --multifile dist/*.asc

freshmeat:
	@echo RETURN to submit to freshmeat.net using freshmeat-submit.txt, CTRL-C to cancel:
	@read DUMMY
	freshmeat-submit < freshmeat-submit.txt

MANIFEST.in: docs
	rm -fv MANIFEST.in
	for i in `ls planes/Vera* NEWS doc/*` ; do echo "include $$i" >> MANIFEST.in ; done
