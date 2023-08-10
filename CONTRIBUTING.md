## Contributors instructions for the Triangle Software members


### How to make a new feature

In a working directory: 

```commandline
git checkout develop
git pull 
git checkout -b your_branch_name/issue_number
```

... do you task

When you are finished:

```commandline
git status
git add .
git commit -m "some_message_for_the_commit, close #issue_number"
git push -u origin your_branch_name/issue_number
```

... and create a pull request to the target branch.