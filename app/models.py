# coding: utf-8
from sqlalchemy import Column, DateTime, ForeignKey, Index, Integer, MetaData, String
from sqlalchemy.schema import FetchedValue
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
metadata = Base.metadata


class MsssSession(Base):
    __tablename__ = 'msss_session'

    id = Column(Integer, primary_key=True)
    instance_id = Column(String(45), nullable=False, unique=True)
    name = Column(String(45))
    init_time = Column(DateTime, nullable=False, server_default=FetchedValue())
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    status = Column(Integer, nullable=False, server_default=FetchedValue(
    ), info='0: Created;\\n1: Started;\\n2: Crashed;\\n3: UserCanceled;\\n4: Finished;')
    note = Column(String(200))


class MsssSessionInput(Base):
    __tablename__ = 'msss_session_input'
    __table_args__ = (
        Index('index', 'index', 'fk_session_id'),
    )

    id = Column(Integer, primary_key=True)
    name = Column(String(64))
    index = Column(Integer, nullable=False, server_default=FetchedValue())
    fk_session_id = Column(ForeignKey('msss_session.id'),
                           nullable=False, index=True)
    note = Column(String(200))

    fk_session = relationship(
        # , backref='msss_session_inputs')
        'MsssSession', primaryjoin='MsssSessionInput.fk_session_id == MsssSession.id')


class MsssSessionInputValue(Base):
    __tablename__ = 'msss_session_input_value'

    id = Column(Integer, primary_key=True)
    fk_session_input_id = Column(ForeignKey(
        'msss_session_input.id'), nullable=False, index=True)
    key = Column(String(64), nullable=False)
    index = Column(Integer, nullable=False)
    data_type = Column(Integer, nullable=False)
    v1 = Column(String(64))
    v2 = Column(String(64))
    v3 = Column(String(512), info='Put json config/list here.')

    fk_session_input = relationship(
        'MsssSessionInput', primaryjoin='MsssSessionInputValue.fk_session_input_id == MsssSessionInput.id', backref='msss_session_input_values')


class MsssSessionOutput(Base):
    __tablename__ = 'msss_session_output'
    __table_args__ = (
        Index('index', 'index', 'fk_session_id'),
    )

    id = Column(Integer, primary_key=True)
    name = Column(String(64))
    index = Column(Integer, nullable=False, server_default=FetchedValue())
    fk_session_id = Column(ForeignKey('msss_session.id'),
                           nullable=False, index=True)
    note = Column(String(200))

    fk_session = relationship(
        'MsssSession', primaryjoin='MsssSessionOutput.fk_session_id == MsssSession.id', backref='msss_session_outputs')


class MsssSessionOutputValue(Base):
    __tablename__ = 'msss_session_output_value'

    id = Column(Integer, primary_key=True)
    fk_session_output_id = Column(ForeignKey(
        'msss_session_output.id'), nullable=False, index=True)
    key = Column(String(64), nullable=False)
    index = Column(Integer, nullable=False)
    data_type = Column(Integer, nullable=False)
    v1 = Column(String(64))
    v2 = Column(String(64))
    v3 = Column(String(512), info='Put json config/list here.')

    fk_session_output = relationship(
        'MsssSessionOutput', primaryjoin='MsssSessionOutputValue.fk_session_output_id == MsssSessionOutput.id', backref='msss_session_output_values')


class MsssSessionParameter(Base):
    __tablename__ = 'msss_session_parameter'
    __table_args__ = (
        Index('index', 'index', 'fk_session_id'),
    )

    id = Column(Integer, primary_key=True)
    name = Column(String(64))
    index = Column(Integer, nullable=False, server_default=FetchedValue())
    fk_session_id = Column(ForeignKey('msss_session.id'),
                           nullable=False, index=True)
    note = Column(String(200))

    fk_session = relationship(
        'MsssSession', primaryjoin='MsssSessionParameter.fk_session_id == MsssSession.id', backref='msss_session_parameters')


class MsssSessionParameterValue(Base):
    __tablename__ = 'msss_session_parameter_value'

    id = Column(Integer, primary_key=True)
    fk_session_parameter_id = Column(ForeignKey(
        'msss_session_parameter.id'), nullable=False, index=True)
    key = Column(String(64), nullable=False)
    index = Column(Integer, nullable=False)
    data_type = Column(Integer, nullable=False)
    v1 = Column(String(64))
    v2 = Column(String(64))
    v3 = Column(String(512), info='Put json config/list here.')

    fk_session_parameter = relationship(
        'MsssSessionParameter', primaryjoin='MsssSessionParameterValue.fk_session_parameter_id == MsssSessionParameter.id', backref='msss_session_parameter_values')


class MsswFileResource(Base):
    __tablename__ = 'mssw_file_resource'

    id = Column(Integer, primary_key=True)
    name = Column(String(128), nullable=False)
    host = Column(String(64))
    fulll_path = Column(String(512), nullable=False)
    disabled = Column(Integer, server_default=FetchedValue())
    operator_id = Column(ForeignKey('sys_user.id'), index=True)
    operate_time = Column(DateTime, nullable=False,
                          server_default=FetchedValue())
    note = Column(String(200))

    operator = relationship(
        'SysUser', primaryjoin='MsswFileResource.operator_id == SysUser.id', backref='mssw_file_resources')


class MsswProces(Base):
    __tablename__ = 'mssw_process'

    id = Column(Integer, primary_key=True)
    fk_program_id = Column(ForeignKey('mssw_program.id'),
                           nullable=False, index=True)
    fk_program_config_id = Column(ForeignKey(
        'mssw_program_config.id'), index=True)
    status = Column(Integer)
    processor_id = Column(Integer)
    start_time = Column(DateTime, nullable=False,
                        server_default=FetchedValue())
    finish_time = Column(DateTime)
    note = Column(String(200))

    fk_program_config = relationship(
        'MsswProgramConfig', primaryjoin='MsswProces.fk_program_config_id == MsswProgramConfig.id', backref='mssw_process')
    fk_program = relationship(
        'MsswProgram', primaryjoin='MsswProces.fk_program_id == MsswProgram.id', backref='mssw_process')


class MsswProcessModelInput(Base):
    __tablename__ = 'mssw_process_model_input'

    id = Column(Integer, primary_key=True)
    name = Column(String(64))
    index = Column(Integer, nullable=False, unique=True,
                   server_default=FetchedValue())
    fk_process_id = Column(Integer, nullable=False, unique=True)
    note = Column(String(200))


class MsswProcessModelInputValue(Base):
    __tablename__ = 'mssw_process_model_input_value'

    id = Column(Integer, primary_key=True)
    fk_process_model_input_id = Column(ForeignKey(
        'mssw_process_model_input.id'), nullable=False, index=True)
    key = Column(String(64), nullable=False)
    index = Column(Integer, nullable=False)
    data_type = Column(Integer, nullable=False)
    v1 = Column(String(64))
    v2 = Column(String(64))
    v3 = Column(String(512), info='Put json config/list here.')

    fk_process_model_input = relationship(
        'MsswProcessModelInput', primaryjoin='MsswProcessModelInputValue.fk_process_model_input_id == MsswProcessModelInput.id', backref='mssw_process_model_input_values')


class MsswProcessModelLog(Base):
    __tablename__ = 'mssw_process_model_log'

    id = Column(Integer, primary_key=True)
    name = Column(String(64))
    index = Column(Integer, nullable=False, unique=True,
                   server_default=FetchedValue())
    fk_process_id = Column(Integer, nullable=False, unique=True)
    note = Column(String(200))


class MsswProcessModelLogValue(Base):
    __tablename__ = 'mssw_process_model_log_value'

    id = Column(Integer, primary_key=True)
    fk_process_model_log_id = Column(ForeignKey(
        'mssw_process_model_log.id'), nullable=False, index=True)
    key = Column(String(64), nullable=False)
    index = Column(Integer, nullable=False)
    data_type = Column(Integer, nullable=False)
    v1 = Column(String(64))
    v2 = Column(String(64))
    v3 = Column(String(512), info='Put json config/list here.')

    fk_process_model_log = relationship(
        'MsswProcessModelLog', primaryjoin='MsswProcessModelLogValue.fk_process_model_log_id == MsswProcessModelLog.id', backref='mssw_process_model_log_values')


class MsswProcessModelOutput(Base):
    __tablename__ = 'mssw_process_model_output'

    id = Column(Integer, primary_key=True)
    name = Column(String(64))
    index = Column(Integer, nullable=False, unique=True,
                   server_default=FetchedValue())
    fk_process_id = Column(Integer, nullable=False, unique=True)
    note = Column(String(200))


class MsswProcessModelOutputValue(Base):
    __tablename__ = 'mssw_process_model_output_value'

    id = Column(Integer, primary_key=True)
    fk_process_model_output_id = Column(ForeignKey(
        'mssw_process_model_output.id'), nullable=False, index=True)
    key = Column(String(64), nullable=False)
    index = Column(Integer, nullable=False)
    data_type = Column(Integer, nullable=False)
    v1 = Column(String(64))
    v2 = Column(String(64))
    v3 = Column(String(512), info='Put json config/list here.')

    fk_process_model_output = relationship(
        'MsswProcessModelOutput', primaryjoin='MsswProcessModelOutputValue.fk_process_model_output_id == MsswProcessModelOutput.id', backref='mssw_process_model_output_values')


class MsswProcessModelParameter(Base):
    __tablename__ = 'mssw_process_model_parameter'

    id = Column(Integer, primary_key=True)
    name = Column(String(64))
    index = Column(Integer, nullable=False, unique=True,
                   server_default=FetchedValue())
    fk_process_id = Column(Integer, nullable=False, unique=True)
    note = Column(String(200))


class MsswProcessModelParameterValue(Base):
    __tablename__ = 'mssw_process_model_parameter_value'

    id = Column(Integer, primary_key=True)
    fk_process_model_parameter_id = Column(ForeignKey(
        'mssw_process_model_parameter.id'), nullable=False, index=True)
    key = Column(String(64), nullable=False)
    index = Column(Integer, nullable=False)
    data_type = Column(Integer, nullable=False)
    v1 = Column(String(64))
    v2 = Column(String(64))
    v3 = Column(String(512), info='Put json config/list here.')

    fk_process_model_parameter = relationship(
        'MsswProcessModelParameter', primaryjoin='MsswProcessModelParameterValue.fk_process_model_parameter_id == MsswProcessModelParameter.id', backref='mssw_process_model_parameter_values')


class MsswProcessRecordAcces(Base):
    __tablename__ = 'mssw_process_record_access'

    id = Column(Integer, primary_key=True)
    fk_process_id = Column(ForeignKey('mssw_process.id'),
                           nullable=False, index=True)
    fk_dict_record_type = Column(ForeignKey(
        'pub_dict.id'), nullable=False, index=True)
    target_type = Column(Integer, nullable=False)
    target_id = Column(Integer, nullable=False)
    disabled = Column(Integer, server_default=FetchedValue())
    operator_id = Column(ForeignKey('sys_user.id'), index=True)
    operate_time = Column(DateTime, server_default=FetchedValue())

    pub_dict = relationship(
        'PubDict', primaryjoin='MsswProcessRecordAcces.fk_dict_record_type == PubDict.id', backref='mssw_process_record_access')
    fk_process = relationship(
        'MsswProces', primaryjoin='MsswProcessRecordAcces.fk_process_id == MsswProces.id', backref='mssw_process_record_access')
    operator = relationship(
        'SysUser', primaryjoin='MsswProcessRecordAcces.operator_id == SysUser.id', backref='mssw_process_record_access')


class MsswProgram(Base):
    __tablename__ = 'mssw_program'

    id = Column(Integer, primary_key=True)
    fk_utility_id = Column(ForeignKey('mssw_ultility.id'),
                           nullable=False, index=True)
    version = Column(String(45), nullable=False)
    fk_provider_employee_id = Column(ForeignKey('sys_employee.id'), index=True)
    description = Column(String(200))
    operator_id = Column(ForeignKey('sys_user.id'),
                         index=True, info='User ID.')
    operate_time = Column(DateTime, nullable=False,
                          server_default=FetchedValue())
    disabled = Column(Integer, nullable=False, server_default=FetchedValue())

    fk_provider_employee = relationship(
        'SysEmployee', primaryjoin='MsswProgram.fk_provider_employee_id == SysEmployee.id', backref='mssw_programs')
    fk_utility = relationship(
        'MsswUltility', primaryjoin='MsswProgram.fk_utility_id == MsswUltility.id', backref='mssw_programs')
    operator = relationship(
        'SysUser', primaryjoin='MsswProgram.operator_id == SysUser.id', backref='mssw_programs')


class MsswProgramActivation(Base):
    __tablename__ = 'mssw_program_activation'

    id = Column(Integer, primary_key=True)
    fk_program_id = Column(ForeignKey('mssw_program.id'),
                           nullable=False, index=True)
    fk_dict_activate_type = Column(ForeignKey(
        'pub_dict.id'), nullable=False, index=True)
    is_active = Column(Integer, nullable=False, server_default=FetchedValue())
    note = Column(String(45))
    operator_id = Column(ForeignKey('sys_user.id'), index=True)
    operate_time = Column(DateTime, nullable=False,
                          server_default=FetchedValue())

    pub_dict = relationship(
        'PubDict', primaryjoin='MsswProgramActivation.fk_dict_activate_type == PubDict.id', backref='mssw_program_activations')
    fk_program = relationship(
        'MsswProgram', primaryjoin='MsswProgramActivation.fk_program_id == MsswProgram.id', backref='mssw_program_activations')
    operator = relationship(
        'SysUser', primaryjoin='MsswProgramActivation.operator_id == SysUser.id', backref='mssw_program_activations')


class MsswProgramConfig(Base):
    __tablename__ = 'mssw_program_config'

    id = Column(Integer, primary_key=True)
    name = Column(String(128), nullable=False)
    fk_program_id = Column(ForeignKey('mssw_program.id'),
                           nullable=False, index=True)
    fk_dict_program_cfg_type = Column(ForeignKey(
        'pub_dict.id'), nullable=False, index=True, info='1: json string\\n2: config file')
    config_value = Column(String(
        2048), info='Type 1: json string;\\nType 2: file path with host address;')
    operator_id = Column(ForeignKey('sys_user.id'), index=True)
    operate_time = Column(DateTime, nullable=False,
                          server_default=FetchedValue())
    disabled = Column(Integer, server_default=FetchedValue())

    pub_dict = relationship(
        'PubDict', primaryjoin='MsswProgramConfig.fk_dict_program_cfg_type == PubDict.id', backref='mssw_program_configs')
    fk_program = relationship(
        'MsswProgram', primaryjoin='MsswProgramConfig.fk_program_id == MsswProgram.id', backref='mssw_program_configs')
    operator = relationship(
        'SysUser', primaryjoin='MsswProgramConfig.operator_id == SysUser.id', backref='mssw_program_configs')


class MsswProgramConfigAcces(Base):
    __tablename__ = 'mssw_program_config_access'

    id = Column(Integer, primary_key=True)
    fk_program_config_id = Column(ForeignKey('mssw_program_config.id'), ForeignKey(
        'mssw_program_config.id'), nullable=False, index=True)
    target_type = Column(Integer, nullable=False,
                         info='1: target_id => User ID\\n2: target_id => Department ID')
    target_id = Column(Integer)
    operator_id = Column(ForeignKey('sys_user.id'), index=True)
    operate_time = Column(DateTime, nullable=False,
                          server_default=FetchedValue())
    disabled = Column(Integer, server_default=FetchedValue())

    fk_program_config = relationship('MsswProgramConfig', primaryjoin='MsswProgramConfigAcces.fk_program_config_id == MsswProgramConfig.id',
                                     backref='msswprogramconfig_mssw_program_config_access')
    fk_program_config1 = relationship('MsswProgramConfig', primaryjoin='MsswProgramConfigAcces.fk_program_config_id == MsswProgramConfig.id',
                                      backref='msswprogramconfig_mssw_program_config_access_0')
    operator = relationship(
        'SysUser', primaryjoin='MsswProgramConfigAcces.operator_id == SysUser.id', backref='mssw_program_config_access')


class MsswUltility(Base):
    __tablename__ = 'mssw_ultility'
    __table_args__ = (
        Index('utility_fk_dict_sub_group_id_2_pub_dict_idx',
              'fk_dict_utility_main_group_id', 'fk_dict_utility_sub_group_id'),
    )

    id = Column(Integer, primary_key=True)
    name = Column(String(64), nullable=False)
    display_name = Column(String(128), nullable=False)
    fk_dict_utility_main_group_id = Column(
        ForeignKey('pub_dict.id'), nullable=False, index=True)
    fk_dict_utility_sub_group_id = Column(
        ForeignKey('pub_dict.id'), nullable=False, index=True)
    disabled = Column(Integer, nullable=False, server_default=FetchedValue())
    operator_id = Column(ForeignKey('sys_user.id'), index=True)
    operate_time = Column(DateTime, nullable=False,
                          server_default=FetchedValue())
    description = Column(String(200))

    fk_dict_utility_main_group = relationship(
        'PubDict', primaryjoin='MsswUltility.fk_dict_utility_main_group_id == PubDict.id', backref='pubdict_mssw_ultilities')
    fk_dict_utility_sub_group = relationship(
        'PubDict', primaryjoin='MsswUltility.fk_dict_utility_sub_group_id == PubDict.id', backref='pubdict_mssw_ultilities_0')
    operator = relationship(
        'SysUser', primaryjoin='MsswUltility.operator_id == SysUser.id', backref='mssw_ultilities')


class PubDict(Base):
    __tablename__ = 'pub_dict'

    id = Column(Integer, primary_key=True)
    name = Column(String(45), nullable=False)
    category = Column(String(45), nullable=False)
    disabled = Column(Integer, nullable=False, server_default=FetchedValue())
    operator_id = Column(Integer)
    operate_time = Column(DateTime, nullable=False,
                          server_default=FetchedValue())
    note = Column(String(200))


class SysCompany(Base):
    __tablename__ = 'sys_company'

    id = Column(Integer, primary_key=True)
    name = Column(String(64), nullable=False, unique=True)
    note = Column(String(200))
    disabled = Column(Integer, nullable=False, server_default=FetchedValue())
    operator_id = Column(Integer)
    operate_time = Column(DateTime, nullable=False,
                          server_default=FetchedValue())


class SysDepartment(Base):
    __tablename__ = 'sys_department'

    id = Column(Integer, primary_key=True)
    name = Column(String(64), nullable=False, unique=True)
    note = Column(String(200))
    fk_sys_company_id = Column(ForeignKey('sys_company.id'), index=True)
    disabled = Column(Integer, nullable=False, server_default=FetchedValue())
    operator_id = Column(String(45))
    operate_time = Column(DateTime, nullable=False,
                          server_default=FetchedValue())

    fk_sys_company = relationship(
        'SysCompany', primaryjoin='SysDepartment.fk_sys_company_id == SysCompany.id', backref='sys_departments')


class SysEmployee(Base):
    __tablename__ = 'sys_employee'

    id = Column(Integer, primary_key=True)
    name = Column(String(64), nullable=False, unique=True)
    note = Column(String(200))
    fk_sys_department_id = Column(ForeignKey('sys_department.id'), index=True)
    disabled = Column(Integer, nullable=False, server_default=FetchedValue())
    operator_id = Column(Integer)
    operate_time = Column(DateTime, nullable=False,
                          server_default=FetchedValue())

    fk_sys_department = relationship(
        'SysDepartment', primaryjoin='SysEmployee.fk_sys_department_id == SysDepartment.id', backref='sys_employees')


class SysUser(Base):
    __tablename__ = 'sys_user'

    id = Column(Integer, primary_key=True)
    name = Column(String(64), nullable=False, unique=True)
    email = Column(String(64))
    fk_sys_employee_id = Column(ForeignKey('sys_employee.id'), index=True)
    disabled = Column(Integer, nullable=False, server_default=FetchedValue())
    operator_id = Column(Integer)
    operate_time = Column(DateTime, nullable=False,
                          server_default=FetchedValue())

    fk_sys_employee = relationship(
        'SysEmployee', primaryjoin='SysUser.fk_sys_employee_id == SysEmployee.id', backref='sys_users')
