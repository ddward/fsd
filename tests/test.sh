python test.py

if curl nginx | grep -q '<a href="/">Financial Statement Data<a>'; then
  exit 0
else
  echo "Tests failed, site offline!"
  exit 1
fi