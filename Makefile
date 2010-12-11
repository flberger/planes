help:
	@echo Targets: docs, clean, user_install

docs: clean
	/home/florian/temp/python/pydoctor/bin/pydoctor --verbose \
	                                                --add-package clickndrag \
	                                                --make-html \
                                                    --html-output doc/

clean:
	rm -fv *.pyc
	rm -fv */*.pyc

user_install:
	python3 setup.py install --user
