#!/bin/sh

if [ -z "$GH_TOKEN" ] || [ -z "$GH_MAIL" ] || [ -z "$GH_NAME" ]; then
  echo "Environment configuration missing, exiting... "
  echo "Token: $GH_TOKEN"
  echo "Mail: $GH_MAIL"
  echo "Name: $GH_NAME"
  exit 1
fi

TEMP_DIR="temp_$GITHUB_SHA"
REPO=$GITHUB_REPOSITORY
DOCS_DIR="docs/"
BUILD_DIR="build/"
HTML_DIR="build/html/"

# Build documentation
# ./build-docs.sh
sphinx-build -M html $DOCS_DIR $BUILD_DIR

# Disable Safe Repository checks
git config --global --add safe.directory "/github/workspace"
git config --global --add safe.directory "/github/workspace/$TEMP_DIR"

# Clone wiki
echo "Cloning gh-pages..."
git clone --branch gh-pages https://$GH_NAME:$GH_TOKEN@github.com/$REPO.git $TEMP_DIR

# Get commit message
message=$(git log -1 --format=%B)
echo "Message:"
echo $message

# Copy files
echo "Copying files to gh-pages"
rsync -av --delete $HTML_DIR $TEMP_DIR/ --exclude .git

# Remove build files
rm -rdf $BUILD_DIR

# Setup credentials for gh-pages
cd $TEMP_DIR
git config user.name $GH_NAME
git config user.email $GH_MAIL

# Push to Wiki
echo "Pushing to gh-pages"
pushd $TEMP_DIR
git add .
git commit -m "$message"
git push origin mastergh-pages
