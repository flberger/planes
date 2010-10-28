help:
	@echo Targets: docs, clean

docs: 
	rm -fv *.pyc
	/home/florian/temp/python/pydoctor/bin/pydoctor --verbose \
	                                                --add-module clickndrag.py \
	                                                --make-html \
	                                                --html-output doc/

clean:
	rm -fv *.pyc
	rm -fv */*.pyc
