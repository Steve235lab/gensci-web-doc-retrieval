# git项目团队协作开发  

## 仓库（Repository）
仓库是git的基本概念，本质就是一个文件目录，这个目录中的所有文件都被git管理，目录下不管做什么操作都会被记录，包括：增加、删除、修改文件等，都会被记录下来，以便后来跟踪与修改相关记录，甚至可以还原到项目中的某个点。从项目的开始到结束，我们有两种仓库。一种是源仓库（origin），一种是本地开发者仓库。  

**源仓库的有两个作用：**  

1. 汇总参与该项目的各个开发者的代码  
2. 存放趋于稳定和可发布的代码  

**开发者仓库**  

源仓库建立以后，每个开发者需要做的事情就是把源仓库clone到本地，作为自己日常开发的仓库。以github for windows软件为例，通过Clone repository就可以将指定的仓库克隆到本地，同时本地的仓库与远程源仓库是关联的，随时可以通过push或pull等操作与源仓库进行交互。
每个开发者的本地仓库共享同一个源仓库，为分离每个人的工作应在仓库自己对应的分支进行操作，实现分布式工作。
## 分支（branch）
分支是git中非常重要的一个概念，是用来将特性开发绝缘开来的。使用分支意味着你可以把你的工作从开发主线上分离开来，在项目的开发中会频繁使用git提供的创建分支、合并分支和删除分支的操作。**一般多人合作的话，可以给团队中的每个人都新建一个开发分支，这样会便于管理。**

当每个人在自己的分支完成开发后，可以通过github的pull request方式将分支上的内容合并到master，存在三种合并方式：  

**第一种，Create a merge commit.**  

这种是最完整的合并方式，以这种方式合并时不仅会保留所有的提交版本，还保留了所有的修改轨迹  

<img src="https://img-blog.csdnimg.cn/2020010118571953.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2FiYzE1ODM3OTk4NDQ4,size_16,color_FFFFFF,t_70" width="50%">
 
**第二种，Squash and merge**  

如图所示，这种方式是最不完整的合并方式，既不保留历史版本，也不保留修改轨迹  

<img src="https://img-blog.csdnimg.cn/2020010118581877.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2FiYzE1ODM3OTk4NDQ4,size_16,color_FFFFFF,t_70" width="30%">

**第三种，Rebase and merge**  

这种方式是前两者的中间值，它保留了提交版本，却不保留各版本的修改轨迹  
<img src="https://img-blog.csdnimg.cn/20200101185751325.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2FiYzE1ODM3OTk4NDQ4,size_16,color_FFFFFF,t_70" width="50%">

 

## Git常用指令
**第一步**，从GitHub上下载项目代码    

	git clone </path/to/repository>
**第二步**，将工作区的代码提交到暂存区  

在本地项目所处的位置右键打开git bash  

输入下面的指令，将工作区的代码提交到暂存区  

	git add <filename>	#只将目标文件添加到暂存区
	git add . 		#将全部修改添加到暂存区
**第三步**，将暂存区的代码提交到仓库区  

	git commit -m "修改信息"
**第四步**，将仓库区的内容提交到远程仓库上  

	git push origin <branch>
**第五步**，更新本地代码  

	git pull
## 分支相关指令
**创建分支**  

进入项目根目录下后，执行下面的指令新建一个分支（复制当前分支，默认为master），括号内是新分支的名字。

	git checkout -b <branch>

**合并分支**  

这条指令会合并其他分支到当前分支

 	git merge <branch>

**将分支推送到远程仓库**  

该指令和修改本地代码后推送到远程仓库是一样的，是将新建的分支内容更新到github上面。除非我们将分支成功推送到远程仓库端，否则该仓库不被团队中他人可见。

	git push origin <branch>

**拉取master分支内容到本地**

	git pull

**切换分支**

	git checkout <branch>

**删掉分支**

	git branch -d <branch>


