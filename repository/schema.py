import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyConnectionField, SQLAlchemyObjectType
from repository.database import db_session
from repository.database import Patient as PatientModel
from sqlalchemy import and_


class Patient(SQLAlchemyObjectType):
    class Meta:
        model = PatientModel
        interfaces = (relay.Node, )


# Used to Create New Patient
class createPatient(graphene.Mutation):
    class Arguments:
        name = graphene.String()
        email = graphene.String()
        username = graphene.String()
    ok = graphene.Boolean()
    patient = graphene.Field(Patient)

    # @classmethod
    # def mutate(cls, _, args, context, info):
    def mutate(self, info, **args):
        patient = PatientModel(name=args.get("name"), email=args.get("email"), username=args.get("username"))
        db_session.add(patient)
        db_session.commit()
        ok = True
        return createPatient(patient=patient, ok=ok)


# Used to Change Username with Email
# class changeUsername(graphene.Mutation):
# 	class Input:
# 		username = graphene.String()
# 		email = graphene.String()
#
# 	ok = graphene.Boolean()
# 	user = graphene.Field(Users)
#
# 	@classmethod
# 	def mutate(cls, _, args, context, info):
# 		query = Users.get_query(context)
# 		email = args.get('email')
# 		username = args.get('username')
# 		user = query.filter(PatientModel.email == email).first()
# 		user.username = username
# 		db_session.commit()
# 		ok = True
#
# 		return changeUsername(user=user, ok = ok)


class Query(graphene.ObjectType):
    node = relay.Node.Field()
    patient = SQLAlchemyConnectionField(Patient)
    find_patient = graphene.Field(lambda: Patient, username=graphene.String())
    all_patients = SQLAlchemyConnectionField(Patient)

    def resolve_find_patient(self, info, **args):
        query = Patient.get_query(info)
        username = args.get('username')
        # you can also use and_ with filter() eg: filter(and_(param1, param2)).first()
        return query.filter(PatientModel.username == username).first()


class MyMutations(graphene.ObjectType):
    create_patient = createPatient.Field()
    # change_username = changeUsername.Field()


schema = graphene.Schema(query=Query, mutation=MyMutations, types=[Patient])
