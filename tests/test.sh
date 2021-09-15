if curl nginx | grep -q '<a href="/">Financial Statement Data<a>'; then
  echo "Tests passed!"
  exit 0
else
  echo "Tests failed!"
  exit 1
fi