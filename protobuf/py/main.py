import addressbook_pb2
p = addressbook_pb2.Person()

p.id = 1234
p.name = "John Doe"
p.email = "jobd@example.com"
phone = p.phone.add()
phone.number = "555-4321"
phone.type = addressbook_pb2.Person.HOME
