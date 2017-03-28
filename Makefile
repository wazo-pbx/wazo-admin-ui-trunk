install:
	python setup.py install
	cp etc/wazo-admin-ui/conf.d/trunk.yml /etc/wazo-admin-ui/conf.d
	systemctl restart wazo-admin-ui

uninstall:
	pip uninstall wazo-admin-ui-trunk
	rm /etc/wazo-admin-ui/conf.d/trunk.yml
	systemctl restart wazo-admin-ui
