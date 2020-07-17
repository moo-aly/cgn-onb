import graphene
from celery.utils.serialization import jsonify
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyConnectionField, SQLAlchemyObjectType
from repository.database import db_session
from repository.database import Patient as PatientModel
from repository.database import Claim as ClaimModel
from sqlalchemy import and_, select
from graphene_file_upload.scalars import Upload
import service_ops.tasks as tasks


class Patient(SQLAlchemyObjectType):
    class Meta:
        model = PatientModel
        interfaces = (relay.Node, )


class Claim(SQLAlchemyObjectType):
    class Meta:
        model = ClaimModel
        interfaces = (relay.Node, )


class createPatient(graphene.Mutation):
    class Arguments:
        name = graphene.String()
        email = graphene.String()
        username = graphene.String()
        mobile = graphene.String()

    ok = graphene.Boolean()
    patient = graphene.Field(Patient)

    # @classmethod
    # def mutate(cls, _, args, context, info):
    def mutate(self, info, **args):
        patient = PatientModel(name=args.get("name"), email=args.get("email"), username=args.get("username"), mobile=args.get("mobile"))
        db_session.add(patient)
        db_session.commit()
        ok = True
        return createPatient(patient=patient, ok=ok)


class createClaim(graphene.Mutation):
    class Arguments:
        reason = graphene.String()
        submission_date = graphene.DateTime()
        total_value = graphene.Float()
        username = graphene.String()
        claim_file = Upload(required=True)

    ok = graphene.Boolean()
    claim = graphene.Field(Claim)

    def mutate(self, info, claim_file, **args):
        claim_object = ClaimModel(reason=args.get("reason"), submission_date=args.get("submission_date"),
                                  total_value=args.get("total_value"), file_name=claim_file.filename)
        patient = PatientModel.query.filter_by(username=args.get("username")).first()
        if patient is not None:
            claim_object.patient_id = patient.id
            claim_object.patient = patient
        # claim_file.save(dst=claim_file.filename)
        tasks.save_file.delay(claim_file.read(), claim_file.filename, claim_file.name, claim_file.content_length, claim_file.content_type, claim_file.headers)
        db_session.add(claim_object)
        db_session.commit()
        ok = True
        return createClaim(claim=claim_object, ok=ok)


class Query(graphene.ObjectType):
    node = relay.Node.Field()
    patient = SQLAlchemyConnectionField(Patient)
    claim = SQLAlchemyConnectionField(Claim)
    all_patients = SQLAlchemyConnectionField(Patient)
    all_claims = SQLAlchemyConnectionField(Claim)
    find_patient_claim = graphene.Field(lambda: Patient, username=graphene.String())

    def resolve_find_patient_claim(self, info, **args):
        query = Patient.get_query(info)
        username = args.get('username')
        # you can also use and_ with filter() eg: filter(and_(param1, param2)).first()
        return query.filter(PatientModel.username == username).first()


class MyMutations(graphene.ObjectType):
    create_patient = createPatient.Field()
    create_claim = createClaim.Field()


schema = graphene.Schema(query=Query, mutation=MyMutations, types=[Patient, Claim, Upload])
