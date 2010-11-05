help:
	@echo Targets: docs, clean

docs: clean
	/home/florian/temp/python/pydoctor/bin/pydoctor --verbose \
	                                                --add-package clickndrag \
	                                                --make-html \
	                                                --html-output doc/

clean:
	rm -fv *.pyc
	rm -fv */*.pyc
