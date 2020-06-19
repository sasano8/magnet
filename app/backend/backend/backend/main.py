import os


def get_leaf(root):
    arr = sorted(os.listdir(root))
    for item in arr:
        yield item



def show_leaf(root, indent: int):
    basename = os.path.basename(root)
    files = list(get_leaf(root))
    if len(files) == 0:
      print(" " * indent + '- {}: []'.format(basename))
    else:
      print(" " * indent + "- {}:".format(basename))
      for item in files:
        branch_root = os.path.join(root, item)

        if os.path.isfile(branch_root):
          print(" " * (indent + 2) + "- {}".format(item))
        else:
          show_leaf(branch_root, indent=indent + 2)



if __name__ == "__main__":
    # app()
    root = "."

    #for item in get_leaf(root):
    #	print(item)

    show_leaf(root, 0)


    
