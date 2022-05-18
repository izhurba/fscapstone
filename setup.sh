#!/bin/bash
export DATABASE_URL="postgresql://postgres:password@localhost:5432/repairshop"
export EXCITED="true"
export AUTHDOMAIN="https://dev-vqzjqwjq.us.auth0.com"
export AUTHCLIENT="TUWUbKOBYQXR4oZ0xwB4CjLjwypkx787"
export REDIRECTURL="http://localhost:5000/"

echo "setup.sh script executed successfully!"

#curl --request GET 'http://localhost:5000/seniortechs' -H "Authorization: Bearer ${STOKEN}" | jq .

# Email: fieldtech@email.com Pass: Fieldtestpass123
# Email: leadtech@email.com Pass: Leadtestpass123
# Email: seniortech@email.com Pass: Seniortestpass123