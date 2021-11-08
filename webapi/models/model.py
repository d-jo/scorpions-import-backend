
# %%
import json

def from_dict(o, d):
    """
    Update a model from a dictionary
    """
    for k, v in d.items():
        setattr(o, k, v)

class BaseModel:
  """
  Base for all models that contians useful functions
  """
  def init_from_dict(self, d):
    for k, v in d.items():
      setattr(self, k, v)
  
  def to_dict(self):
    d = {}
    for attr in self.__slots__:
      if attr[0] != '_':
        d[attr] = getattr(self, attr)
    return d

class Report(BaseModel):
  __slots__ = [
    'id',
    'title',
    'author',
    'created',
    'college',
    'department',
    'program',
    'degree_level',
    'academic_year',
    'date_range',
    'accreditation_body',
    'last_accreditation_review',
    'slos_meet_standards',
    'stakeholder_involvement',
    'additional_information'
  ]
  def __init__(self):
    self.id = ""
    self.title = ""
    self.author = ""
    self.created = ""
    self.college = ""
    self.department = ""
    self.program = ""
    self.degree_level = ""
    self.academic_year = ""
    self.date_range = ""
    self.accreditation_body = ""
    self.last_accreditation_review = ""
    self.slos_meet_standards = ""
    self.stakeholder_involvement = ""
    self.additional_information = ""
    pass


class SLO(BaseModel):
  __slots__ = [
    'id',
    'description',
    'bloom',
    'common_graduate_program_slo'
  ]
  def __init__(self):
    self.id = ""
    self.description = ""
    self.bloom = ""
    self.common_graduate_program_slo = ""
    pass

class Measure(BaseModel):
  __slots__ = [
    'id',
    'slo_id',
    'title',
    'description',
    'domain',
    'type',
    'point_in_program',
    'population_measured',
    'frequency_of_collection',
    'proficiency_threshold',
    'proficiency_target'
  ]
  def __init__(self):
    self.id = ""
    self.slo_id = ""
    self.title = ""
    self.description = ""
    self.domain = ""
    self.type = ""
    self.point_in_program = ""
    self.population_measured = ""
    self.frequency_of_collection = ""
    self.proficiency_threshold = ""
    self.proficiency_target = ""
    pass

class DecisionsAction(BaseModel):
  __slots__ = [
    'id',
    'slo_id',
    'content'
  ]
  def __init__(self):
    self.id = ""
    self.slo_id = ""
    self.content = ""
    pass

class CollectionAnalysis(BaseModel):
  __slots__ = [
    'id',
    'slo_id',
    'data_collection_date_range',
    'number_of_students_assessed',
    'percentage_who_met_or_exceeded'
  ]
  def __init__(self):
    self.id = ""
    self.slo_id = ""
    self.data_collection_date_range = ""
    self.number_of_students_assessed = ""
    self.percentage_who_met_or_exceeded = ""
    pass

class Methods(BaseModel):
  __slots__ = [
    'id',
    'slo_id',
    'measure',
    'domain',
    'data_collection'
  ]
  def __init__(self):
    self.id = ""
    self.slo_id = ""
    self.measure = ""
    self.domain = ""
    self.data_collection = ""
    pass

class AccreditedDataAnalysis(BaseModel):
  __slots__ = [
    'id',
    'slo_id',
    'status'
  ]
  def __init__(self):
    self.id = ""
    self.slo_id = ""
    self.status = ""
    pass
