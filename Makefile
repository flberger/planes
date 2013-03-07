help:
	@echo Targets:
	@echo '    docs'
	@echo '    clean'
	@echo '    pylint'
	@echo '    errors'
	@echo '    user_install'
	@echo '    sdist'
	@echo '    exe'
	@echo '    commit.txt'
	@echo '    commit'
	@echo '    sign'
	@echo '    freecode'
	@echo '    pypi'
	@echo '    lp'
	@echo '    README.rst'

docs: clean
	pydoctor --verbose \
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

sdist: resources.zip
	$(PYTHON) setup.py sdist --force-manifest --formats=zip

pypi:
	$(PYTHON) setup.py register

exe: sdist
	rm -rf build/exe.*
	$(PYTHON) setup.py build

else

user_install:
	@echo Please supply Python executable as PYTHON=executable.

sdist:
	@echo Please supply Python executable as PYTHON=executable.

pypi:
	@echo Please supply Python executable as PYTHON=executable.

exe: sdist
	@echo Please supply Python executable as PYTHON=executable.

endif

commit.txt:
	# single line because bzr diff returns false when there are diffs
	#
	bzr diff > commit.txt ; nano commit.txt

commit:
	@echo commit.txt:
	@echo ------------------------------------------------------
	@cat commit.txt
	@echo ------------------------------------------------------
	@echo RETURN to commit using commit.txt, CTRL-C to cancel:
	@read DUMMY
	bzr commit --file commit.txt && rm -v commit.txt

sign:
	rm -vf dist/*.asc
	for i in dist/*.*z* ; do gpg --sign --armor --detach $$i ; done
	gpg --verify --multifile dist/*.asc

freecode:
	@echo RETURN to submit to freecode.com using freecode-submit.txt, CTRL-C to cancel:
	@read DUMMY
	freecode-submit < freecode-submit.txt

lp:
	bzr launchpad-login fberger-fbmd
	bzr push lp:~fberger-fbmd/planes/trunk

README.rst: README
	pandoc --output README.rst README

resources.zip:
	cd planes/gui/ && rm -fv resources.zip && find fonts/ gfx/ > MANIFEST && zip -9 -r resources.zip MANIFEST fonts/ gfx/
