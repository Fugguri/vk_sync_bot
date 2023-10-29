update:
	git add .
	git commit -m "update"
	git push

push:
	git push


init-repo:
	echo "# vk_sync_bot" >> README.md
	git init
	git add .
	git commit -m "create"
	git branch -M main
	git remote add origin https://github.com/Fugguri/vk_sync_bot.git
	git push -u origin main