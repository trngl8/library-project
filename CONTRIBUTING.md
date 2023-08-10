## Contributors instructions for the Triangle Software members


### How to make a new feature

In a working directory check the **target_branch**:

```commandline
git checkout target_branch
git pull 
git checkout -b your_branch_name/issue_number
```
Now you may push you branch to the remote repository:

```commandline
git push -u origin your_branch_name/issue_number
```
... do you task

When you are finished:

```commandline
git status
git add .
git commit -m "some_message_for_the_commit, close #issue_number"
git push 
```

... and create a pull request to the target_branch.