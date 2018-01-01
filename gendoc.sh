#!/bin/bash
# Generate the module documentation
# Needs: pydoc and links

function on_error
{
  args="$@"
  if [ ${#args} -lt 1 ]; then
    echo "Usage: $0"
    exit 1
  fi
  echo -e "\033[91mError:\033[0m ${args}"
  exit 1
}

function gendoc
{
  DOCDIR="./doc/"
  PYDOC=$(which pydoc)
  LINKS=$(which links)
  if [ ! -d ${DOCDIR} ]; then
    on_error "Directory not found '${DOCDIR}'. Please make sure you are running this script from within the ants module directory."
  fi
  if [ ${#PYDOC} -eq 0 ]; then
    on_error "Unknown command 'pydoc'. Please check your python installation."
  fi
  if [ ${#LINKS} -eq 0 ]; then
    on_error "Unknown command 'links'. Please install the links terminal web browser."
  fi
  echo -e "\033[92mGenerating documentation:\033[0m"
  for PYFILE in $(find ./ -maxdepth 1 -type f -name "*.py")
  do
    BASENAME=$(basename ${PYFILE} .py)
    HTML="${DOCDIR}/${BASENAME}.html"
    TXT="${DOCDIR}/${BASENAME}.txt"
    echo -e "  \033[093m[+] ${PYFILE}\033[0m"
    ${PYDOC} -w ${PYFILE} >/dev/null
    RET_VAL=$?
    if [ ! ${RET_VAL} -eq 0 ]; then
      on_error "Error while generating documentation for ${PYFILE}"
    fi
    if [ -f "./${BASENAME}.html" ]; then
      mv ./${BASENAME}.html ${HTML}
      ${LINKS} -dump ${HTML} > ${TXT}
    fi
  done
}

if [ $# -gt 0 ]; then
  on_error
fi
gendoc
git add .
