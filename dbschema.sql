--
-- PostgreSQL database dump
--

-- Dumped from database version 12.4
-- Dumped by pg_dump version 12.5 (Ubuntu 12.5-0ubuntu0.20.04.1)
SELECT * FROM "makeReports_report"


SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: auth_group; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.auth_group (
    id integer NOT NULL,
    name character varying(150) NOT NULL
);


ALTER TABLE public.auth_group OWNER TO postgres;

--
-- Name: auth_group_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.auth_group_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_group_id_seq OWNER TO postgres;

--
-- Name: auth_group_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.auth_group_id_seq OWNED BY public.auth_group.id;


--
-- Name: auth_group_permissions; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.auth_group_permissions (
    id integer NOT NULL,
    group_id integer NOT NULL,
    permission_id integer NOT NULL
);


ALTER TABLE public.auth_group_permissions OWNER TO postgres;

--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.auth_group_permissions_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_group_permissions_id_seq OWNER TO postgres;

--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.auth_group_permissions_id_seq OWNED BY public.auth_group_permissions.id;


--
-- Name: auth_permission; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.auth_permission (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    content_type_id integer NOT NULL,
    codename character varying(100) NOT NULL
);


ALTER TABLE public.auth_permission OWNER TO postgres;

--
-- Name: auth_permission_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.auth_permission_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_permission_id_seq OWNER TO postgres;

--
-- Name: auth_permission_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgress
--

ALTER SEQUENCE public.auth_permission_id_seq OWNED BY public.auth_permission.id;


--
-- Name: auth_user; Type: TABLE; Schema: public; Owner: doadmin
--

CREATE TABLE public.auth_user (
    id integer NOT NULL,
    password character varying(128) NOT NULL,
    last_login timestamp with time zone,
    is_superuser boolean NOT NULL,
    username character varying(150) NOT NULL,
    first_name character varying(30) NOT NULL,
    last_name character varying(150) NOT NULL,
    email character varying(254) NOT NULL,
    is_staff boolean NOT NULL,
    is_active boolean NOT NULL,
    date_joined timestamp with time zone NOT NULL
);


ALTER TABLE public.auth_user OWNER TO postgres;

--
-- Name: auth_user_groups; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.auth_user_groups (
    id integer NOT NULL,
    user_id integer NOT NULL,
    group_id integer NOT NULL
);


ALTER TABLE public.auth_user_groups OWNER TO postgres;

--
-- Name: auth_user_groups_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.auth_user_groups_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_user_groups_id_seq OWNER TO postgres;

--
-- Name: auth_user_groups_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.auth_user_groups_id_seq OWNED BY public.auth_user_groups.id;


--
-- Name: auth_user_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.auth_user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_user_id_seq OWNER TO postgres;

--
-- Name: auth_user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.auth_user_id_seq OWNED BY public.auth_user.id;


--
-- Name: auth_user_user_permissions; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.auth_user_user_permissions (
    id integer NOT NULL,
    user_id integer NOT NULL,
    permission_id integer NOT NULL
);


ALTER TABLE public.auth_user_user_permissions OWNER TO postgres;

--
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.auth_user_user_permissions_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_user_user_permissions_id_seq OWNER TO postgres;

--
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.auth_user_user_permissions_id_seq OWNED BY public.auth_user_user_permissions.id;



--
-- Name: makeReports_announcement; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."makeReports_announcement" (
    id integer NOT NULL,
    text character varying(2000) NOT NULL,
    expiration date NOT NULL,
    creation timestamp with time zone NOT NULL
);


ALTER TABLE public."makeReports_announcement" OWNER TO postgres;

--
-- Name: makeReports_announcement_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."makeReports_announcement_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."makeReports_announcement_id_seq" OWNER TO postgres;

--
-- Name: makeReports_announcement_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."makeReports_announcement_id_seq" OWNED BY public."makeReports_announcement".id;


--
-- Name: makeReports_assessment; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."makeReports_assessment" (
    id integer NOT NULL,
    title character varying(300) NOT NULL,
    "domainExamination" boolean NOT NULL,
    "domainProduct" boolean NOT NULL,
    "domainPerformance" boolean NOT NULL,
    "directMeasure" boolean NOT NULL,
    "numberOfUses" integer NOT NULL,
    CONSTRAINT "makeReports_assessment_numberOfUses_check" CHECK (("numberOfUses" >= 0))
);


ALTER TABLE public."makeReports_assessment" OWNER TO postgres;

--
-- Name: makeReports_assessment_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."makeReports_assessment_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."makeReports_assessment_id_seq" OWNER TO postgres;

--
-- Name: makeReports_assessment_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."makeReports_assessment_id_seq" OWNED BY public."makeReports_assessment".id;


--
-- Name: makeReports_assessmentaggregate; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."makeReports_assessmentaggregate" (
    id integer NOT NULL,
    aggregate_proficiency integer NOT NULL,
    met boolean NOT NULL,
    "assessmentVersion_id" integer NOT NULL,
    override boolean NOT NULL,
    CONSTRAINT "makeReports_assessmentaggregate_aggregate_proficiency_check" CHECK ((aggregate_proficiency >= 0))
);


ALTER TABLE public."makeReports_assessmentaggregate" OWNER TO postgres;

--
-- Name: makeReports_assessmentaggregate_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."makeReports_assessmentaggregate_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."makeReports_assessmentaggregate_id_seq" OWNER TO postgres;

--
-- Name: makeReports_assessmentaggregate_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."makeReports_assessmentaggregate_id_seq" OWNED BY public."makeReports_assessmentaggregate".id;


--
-- Name: makeReports_assessmentdata; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."makeReports_assessmentdata" (
    id integer NOT NULL,
    "numberStudents" integer NOT NULL,
    "overallProficient" integer NOT NULL,
    "assessmentVersion_id" integer NOT NULL,
    "dataRange" character varying(500) NOT NULL,
    CONSTRAINT "makeReports_assessmentdata_numberStudents_check" CHECK (("numberStudents" >= 0)),
    CONSTRAINT "makeReports_assessmentdata_overallProficient_check" CHECK (("overallProficient" >= 0))
);


ALTER TABLE public."makeReports_assessmentdata" OWNER TO postgres;

--
-- Name: makeReports_assessmentdata_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."makeReports_assessmentdata_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."makeReports_assessmentdata_id_seq" OWNER TO postgres;

--
-- Name: makeReports_assessmentdata_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."makeReports_assessmentdata_id_seq" OWNED BY public."makeReports_assessmentdata".id;


--
-- Name: makeReports_assessmentsupplement; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."makeReports_assessmentsupplement" (
    id integer NOT NULL,
    supplement character varying(100) NOT NULL,
    uploaded_at timestamp with time zone NOT NULL
);


ALTER TABLE public."makeReports_assessmentsupplement" OWNER TO postgres;

--
-- Name: makeReports_assessmentsupplement_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."makeReports_assessmentsupplement_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."makeReports_assessmentsupplement_id_seq" OWNER TO postgres;

--
-- Name: makeReports_assessmentsupplement_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."makeReports_assessmentsupplement_id_seq" OWNED BY public."makeReports_assessmentsupplement".id;


--
-- Name: makeReports_assessmentversion; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."makeReports_assessmentversion" (
    id integer NOT NULL,
    date date NOT NULL,
    description character varying(1000) NOT NULL,
    "finalTerm" boolean NOT NULL,
    "where" character varying(500) NOT NULL,
    "allStudents" boolean NOT NULL,
    "sampleDescription" character varying(500),
    frequency character varying(500) NOT NULL,
    threshold character varying(500) NOT NULL,
    target integer NOT NULL,
    assessment_id integer NOT NULL,
    report_id integer NOT NULL,
    "changedFromPrior" boolean NOT NULL,
    slo_id integer NOT NULL,
    number integer NOT NULL,
    "frequencyChoice" character varying(100) NOT NULL,
    CONSTRAINT "makeReports_assessmentversion_number_check" CHECK ((number >= 0)),
    CONSTRAINT "makeReports_assessmentversion_target_check" CHECK ((target >= 0))
);


ALTER TABLE public."makeReports_assessmentversion" OWNER TO postgres;

--
-- Name: makeReports_assessmentversion_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."makeReports_assessmentversion_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."makeReports_assessmentversion_id_seq" OWNER TO postgres;

--
-- Name: makeReports_assessmentversion_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."makeReports_assessmentversion_id_seq" OWNED BY public."makeReports_assessmentversion".id;


--
-- Name: makeReports_assessmentversion_supplements; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."makeReports_assessmentversion_supplements" (
    id integer NOT NULL,
    assessmentversion_id integer NOT NULL,
    assessmentsupplement_id integer NOT NULL
);


ALTER TABLE public."makeReports_assessmentversion_supplements" OWNER TO postgres;

--
-- Name: makeReports_assessmentversion_supplements_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."makeReports_assessmentversion_supplements_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."makeReports_assessmentversion_supplements_id_seq" OWNER TO postgres;

--
-- Name: makeReports_assessmentversion_supplements_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."makeReports_assessmentversion_supplements_id_seq" OWNED BY public."makeReports_assessmentversion_supplements".id;


--
-- Name: makeReports_college; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."makeReports_college" (
    id integer NOT NULL,
    name character varying(100) NOT NULL,
    active boolean NOT NULL
);


ALTER TABLE public."makeReports_college" OWNER TO postgres;

--
-- Name: makeReports_college_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."makeReports_college_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."makeReports_college_id_seq" OWNER TO postgres;

--
-- Name: makeReports_college_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."makeReports_college_id_seq" OWNED BY public."makeReports_college".id;


--
-- Name: makeReports_dataadditionalinformation; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."makeReports_dataadditionalinformation" (
    id integer NOT NULL,
    comment character varying(3000) NOT NULL,
    report_id integer NOT NULL,
    supplement character varying(100) NOT NULL
);


ALTER TABLE public."makeReports_dataadditionalinformation" OWNER TO postgres;

--
-- Name: makeReports_dataadditionalinformation_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."makeReports_dataadditionalinformation_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."makeReports_dataadditionalinformation_id_seq" OWNER TO postgres;

--
-- Name: makeReports_dataadditionalinformation_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."makeReports_dataadditionalinformation_id_seq" OWNED BY public."makeReports_dataadditionalinformation".id;


--
-- Name: makeReports_decisionsactions; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."makeReports_decisionsactions" (
    id integer NOT NULL,
    text character varying(3000) NOT NULL,
    "sloIR_id" integer NOT NULL
);


ALTER TABLE public."makeReports_decisionsactions" OWNER TO postgres;

--
-- Name: makeReports_decisionsactions_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."makeReports_decisionsactions_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."makeReports_decisionsactions_id_seq" OWNER TO postgres;

--
-- Name: makeReports_decisionsactions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."makeReports_decisionsactions_id_seq" OWNED BY public."makeReports_decisionsactions".id;


--
-- Name: makeReports_degreeprogram; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."makeReports_degreeprogram" (
    id integer NOT NULL,
    name character varying(100) NOT NULL,
    level character varying(75) NOT NULL,
    cycle integer,
    department_id integer NOT NULL,
    "startingYear" integer,
    active boolean NOT NULL,
    accredited boolean NOT NULL,
    CONSTRAINT "makeReports_degreeprogram_startingYear_check" CHECK (("startingYear" >= 0))
);


ALTER TABLE public."makeReports_degreeprogram" OWNER TO postgres;

--
-- Name: makeReports_degreeprogram_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."makeReports_degreeprogram_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."makeReports_degreeprogram_id_seq" OWNER TO postgres;

--
-- Name: makeReports_degreeprogram_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."makeReports_degreeprogram_id_seq" OWNED BY public."makeReports_degreeprogram".id;


--
-- Name: makeReports_department; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."makeReports_department" (
    id integer NOT NULL,
    name character varying(100) NOT NULL,
    college_id integer NOT NULL,
    active boolean NOT NULL
);


ALTER TABLE public."makeReports_department" OWNER TO postgres;

--
-- Name: makeReports_department_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."makeReports_department_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."makeReports_department_id_seq" OWNER TO postgres;

--
-- Name: makeReports_department_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."makeReports_department_id_seq" OWNED BY public."makeReports_department".id;


--
-- Name: makeReports_gradedrubric; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."makeReports_gradedrubric" (
    id integer NOT NULL,
    "rubricVersion_id" integer NOT NULL,
    "generalComment" character varying(2000),
    "section1Comment" character varying(2000),
    "section2Comment" character varying(2000),
    "section3Comment" character varying(2000),
    "section4Comment" character varying(2000),
    complete boolean NOT NULL
);


ALTER TABLE public."makeReports_gradedrubric" OWNER TO postgres;

--
-- Name: makeReports_gradedrubric_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."makeReports_gradedrubric_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."makeReports_gradedrubric_id_seq" OWNER TO postgres;

--
-- Name: makeReports_gradedrubric_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."makeReports_gradedrubric_id_seq" OWNED BY public."makeReports_gradedrubric".id;


--
-- Name: makeReports_gradedrubricitem; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."makeReports_gradedrubricitem" (
    id integer NOT NULL,
    grade character varying(300) NOT NULL,
    item_id integer NOT NULL,
    rubric_id integer NOT NULL
);


ALTER TABLE public."makeReports_gradedrubricitem" OWNER TO postgres;

--
-- Name: makeReports_gradedrubricitem_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."makeReports_gradedrubricitem_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."makeReports_gradedrubricitem_id_seq" OWNER TO postgres;

--
-- Name: makeReports_gradedrubricitem_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."makeReports_gradedrubricitem_id_seq" OWNED BY public."makeReports_gradedrubricitem".id;


--
-- Name: makeReports_gradgoal; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."makeReports_gradgoal" (
    id integer NOT NULL,
    text character varying(600) NOT NULL,
    active boolean NOT NULL
);


ALTER TABLE public."makeReports_gradgoal" OWNER TO postgres;

--
-- Name: makeReports_gradgoal_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."makeReports_gradgoal_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."makeReports_gradgoal_id_seq" OWNER TO postgres;

--
-- Name: makeReports_gradgoal_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."makeReports_gradgoal_id_seq" OWNED BY public."makeReports_gradgoal".id;


--
-- Name: makeReports_graph; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."makeReports_graph" (
    id integer NOT NULL,
    "dateTime" timestamp with time zone NOT NULL,
    graph character varying(100) NOT NULL
);


ALTER TABLE public."makeReports_graph" OWNER TO postgres;

--
-- Name: makeReports_graph_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."makeReports_graph_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."makeReports_graph_id_seq" OWNER TO postgres;

--
-- Name: makeReports_graph_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."makeReports_graph_id_seq" OWNED BY public."makeReports_graph".id;


--
-- Name: makeReports_profile; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."makeReports_profile" (
    id integer NOT NULL,
    aac boolean,
    department_id integer,
    user_id integer NOT NULL
);


ALTER TABLE public."makeReports_profile" OWNER TO postgres;

--
-- Name: makeReports_profile_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."makeReports_profile_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."makeReports_profile_id_seq" OWNER TO postgres;

--
-- Name: makeReports_profile_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."makeReports_profile_id_seq" OWNED BY public."makeReports_profile".id;


--
-- Name: makeReports_report; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."makeReports_report" (
    id integer NOT NULL,
    author character varying(100) NOT NULL,
    "section1Comment" character varying(2000),
    "section2Comment" character varying(2000),
    "section3Comment" character varying(2000),
    "section4Comment" character varying(2000),
    submitted boolean NOT NULL,
    "degreeProgram_id" integer NOT NULL,
    rubric_id integer,
    year integer NOT NULL,
    returned boolean NOT NULL,
    date_range_of_reported_data character varying(500),
    "numberOfSLOs" integer NOT NULL,
    accredited boolean NOT NULL,
    CONSTRAINT "makeReports_report_numberOfSLOs_check" CHECK (("numberOfSLOs" >= 0)),
    CONSTRAINT "makeReports_report_year_check" CHECK ((year >= 0))
);


ALTER TABLE public."makeReports_report" OWNER TO postgres;

--
-- Name: makeReports_report_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."makeReports_report_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."makeReports_report_id_seq" OWNER TO postgres;

--
-- Name: makeReports_report_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."makeReports_report_id_seq" OWNED BY public."makeReports_report".id;


--
-- Name: makeReports_reportsupplement; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."makeReports_reportsupplement" (
    id integer NOT NULL,
    supplement character varying(100) NOT NULL,
    report_id integer NOT NULL
);


ALTER TABLE public."makeReports_reportsupplement" OWNER TO postgres;

--
-- Name: makeReports_reportsupplement_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."makeReports_reportsupplement_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."makeReports_reportsupplement_id_seq" OWNER TO postgres;

--
-- Name: makeReports_reportsupplement_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."makeReports_reportsupplement_id_seq" OWNED BY public."makeReports_reportsupplement".id;


--
-- Name: makeReports_requiredfieldsetting; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."makeReports_requiredfieldsetting" (
    id integer NOT NULL,
    name character varying(200) NOT NULL,
    required boolean NOT NULL
);


ALTER TABLE public."makeReports_requiredfieldsetting" OWNER TO postgres;

--
-- Name: makeReports_requiredfieldsetting_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."makeReports_requiredfieldsetting_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."makeReports_requiredfieldsetting_id_seq" OWNER TO postgres;

--
-- Name: makeReports_requiredfieldsetting_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."makeReports_requiredfieldsetting_id_seq" OWNED BY public."makeReports_requiredfieldsetting".id;


--
-- Name: makeReports_resultcommunicate; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."makeReports_resultcommunicate" (
    id integer NOT NULL,
    text character varying(3000) NOT NULL,
    report_id integer NOT NULL
);


ALTER TABLE public."makeReports_resultcommunicate" OWNER TO postgres;

--
-- Name: makeReports_resultcommunicate_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."makeReports_resultcommunicate_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."makeReports_resultcommunicate_id_seq" OWNER TO postgres;

--
-- Name: makeReports_resultcommunicate_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."makeReports_resultcommunicate_id_seq" OWNED BY public."makeReports_resultcommunicate".id;


--
-- Name: makeReports_rubric; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."makeReports_rubric" (
    id integer NOT NULL,
    date date NOT NULL,
    "fullFile" character varying(100),
    name character varying(150) NOT NULL
);


ALTER TABLE public."makeReports_rubric" OWNER TO postgres;

--
-- Name: makeReports_rubric_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."makeReports_rubric_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."makeReports_rubric_id_seq" OWNER TO postgres;

--
-- Name: makeReports_rubric_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."makeReports_rubric_id_seq" OWNED BY public."makeReports_rubric".id;


--
-- Name: makeReports_rubricitem; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."makeReports_rubricitem" (
    id integer NOT NULL,
    text character varying(1000) NOT NULL,
    section integer NOT NULL,
    "rubricVersion_id" integer NOT NULL,
    "order" integer,
    "DMEtext" character varying(1000) NOT NULL,
    "EEtext" character varying(1000) NOT NULL,
    "MEtext" character varying(1000) NOT NULL,
    abbreviation character varying(20) NOT NULL,
    CONSTRAINT "makeReports_rubricitem_order_check" CHECK (("order" >= 0)),
    CONSTRAINT "makeReports_rubricitem_section_check" CHECK ((section >= 0))
);


ALTER TABLE public."makeReports_rubricitem" OWNER TO postgres;

--
-- Name: makeReports_rubricitem_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."makeReports_rubricitem_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."makeReports_rubricitem_id_seq" OWNER TO postgres;

--
-- Name: makeReports_rubricitem_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."makeReports_rubricitem_id_seq" OWNED BY public."makeReports_rubricitem".id;


--
-- Name: makeReports_slo; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."makeReports_slo" (
    id integer NOT NULL,
    blooms character varying(50) NOT NULL,
    "numberOfUses" integer NOT NULL,
    CONSTRAINT "makeReports_slo_numberOfUses_check" CHECK (("numberOfUses" >= 0))
);


ALTER TABLE public."makeReports_slo" OWNER TO postgres;

--
-- Name: makeReports_slo_gradGoals; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."makeReports_slo_gradGoals" (
    id integer NOT NULL,
    slo_id integer NOT NULL,
    gradgoal_id integer NOT NULL
);


ALTER TABLE public."makeReports_slo_gradGoals" OWNER TO postgres;

--
-- Name: makeReports_slo_gradGoals_id_seq; Type: SEQUENCE; Schema: public; Owner: doadmin
--

CREATE SEQUENCE public."makeReports_slo_gradGoals_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."makeReports_slo_gradGoals_id_seq" OWNER TO postgres;

--
-- Name: makeReports_slo_gradGoals_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."makeReports_slo_gradGoals_id_seq" OWNED BY public."makeReports_slo_gradGoals".id;


--
-- Name: makeReports_slo_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."makeReports_slo_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."makeReports_slo_id_seq" OWNER TO postgres;

--
-- Name: makeReports_slo_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."makeReports_slo_id_seq" OWNED BY public."makeReports_slo".id;


--
-- Name: makeReports_sloinreport; Type: TABLE; Schema: public; Owner: doadmin
--

CREATE TABLE public."makeReports_sloinreport" (
    id integer NOT NULL,
    report_id integer NOT NULL,
    slo_id integer NOT NULL,
    "changedFromPrior" boolean NOT NULL,
    date date NOT NULL,
    "goalText" character varying(1000) NOT NULL,
    number integer NOT NULL,
    "numberOfAssess" integer NOT NULL,
    CONSTRAINT "makeReports_sloinreport_numberOfAssess_check" CHECK (("numberOfAssess" >= 0)),
    CONSTRAINT "makeReports_sloinreport_number_check" CHECK ((number >= 0))
);


ALTER TABLE public."makeReports_sloinreport" OWNER TO postgres;

--
-- Name: makeReports_sloinreport_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."makeReports_sloinreport_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."makeReports_sloinreport_id_seq" OWNER TO postgres;

--
-- Name: makeReports_sloinreport_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."makeReports_sloinreport_id_seq" OWNED BY public."makeReports_sloinreport".id;


--
-- Name: makeReports_slostatus; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."makeReports_slostatus" (
    id integer NOT NULL,
    status character varying(50) NOT NULL,
    "sloIR_id" integer NOT NULL,
    override boolean NOT NULL
);


ALTER TABLE public."makeReports_slostatus" OWNER TO postgres;

--
-- Name: makeReports_slostatus_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."makeReports_slostatus_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."makeReports_slostatus_id_seq" OWNER TO postgres;

--
-- Name: makeReports_slostatus_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."makeReports_slostatus_id_seq" OWNED BY public."makeReports_slostatus".id;


--
-- Name: makeReports_slostostakeholder; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."makeReports_slostostakeholder" (
    id integer NOT NULL,
    text character varying(2000) NOT NULL,
    report_id integer
);


ALTER TABLE public."makeReports_slostostakeholder" OWNER TO postgres;

--
-- Name: makeReports_slostostakeholder_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."makeReports_slostostakeholder_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."makeReports_slostostakeholder_id_seq" OWNER TO postgres;

--
-- Name: makeReports_slostostakeholder_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."makeReports_slostostakeholder_id_seq" OWNED BY public."makeReports_slostostakeholder".id;


--
-- Name: auth_group id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group ALTER COLUMN id SET DEFAULT nextval('public.auth_group_id_seq'::regclass);


--
-- Name: auth_group_permissions id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group_permissions ALTER COLUMN id SET DEFAULT nextval('public.auth_group_permissions_id_seq'::regclass);


--
-- Name: auth_permission id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_permission ALTER COLUMN id SET DEFAULT nextval('public.auth_permission_id_seq'::regclass);


--
-- Name: auth_user id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_user ALTER COLUMN id SET DEFAULT nextval('public.auth_user_id_seq'::regclass);


--
-- Name: auth_user_groups id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_user_groups ALTER COLUMN id SET DEFAULT nextval('public.auth_user_groups_id_seq'::regclass);


--
-- Name: auth_user_user_permissions id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_user_user_permissions ALTER COLUMN id SET DEFAULT nextval('public.auth_user_user_permissions_id_seq'::regclass);



--
-- Name: makeReports_announcement id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."makeReports_announcement" ALTER COLUMN id SET DEFAULT nextval('public."makeReports_announcement_id_seq"'::regclass);


--
-- Name: makeReports_assessment id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."makeReports_assessment" ALTER COLUMN id SET DEFAULT nextval('public."makeReports_assessment_id_seq"'::regclass);


--
-- Name: makeReports_assessmentaggregate id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."makeReports_assessmentaggregate" ALTER COLUMN id SET DEFAULT nextval('public."makeReports_assessmentaggregate_id_seq"'::regclass);


--
-- Name: makeReports_assessmentdata id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."makeReports_assessmentdata" ALTER COLUMN id SET DEFAULT nextval('public."makeReports_assessmentdata_id_seq"'::regclass);


--
-- Name: makeReports_assessmentsupplement id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."makeReports_assessmentsupplement" ALTER COLUMN id SET DEFAULT nextval('public."makeReports_assessmentsupplement_id_seq"'::regclass);


--
-- Name: makeReports_assessmentversion id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."makeReports_assessmentversion" ALTER COLUMN id SET DEFAULT nextval('public."makeReports_assessmentversion_id_seq"'::regclass);


--
-- Name: makeReports_assessmentversion_supplements id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."makeReports_assessmentversion_supplements" ALTER COLUMN id SET DEFAULT nextval('public."makeReports_assessmentversion_supplements_id_seq"'::regclass);


--
-- Name: makeReports_college id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."makeReports_college" ALTER COLUMN id SET DEFAULT nextval('public."makeReports_college_id_seq"'::regclass);


--
-- Name: makeReports_dataadditionalinformation id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."makeReports_dataadditionalinformation" ALTER COLUMN id SET DEFAULT nextval('public."makeReports_dataadditionalinformation_id_seq"'::regclass);


--
-- Name: makeReports_decisionsactions id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."makeReports_decisionsactions" ALTER COLUMN id SET DEFAULT nextval('public."makeReports_decisionsactions_id_seq"'::regclass);


--
-- Name: makeReports_degreeprogram id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."makeReports_degreeprogram" ALTER COLUMN id SET DEFAULT nextval('public."makeReports_degreeprogram_id_seq"'::regclass);


--
-- Name: makeReports_department id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."makeReports_department" ALTER COLUMN id SET DEFAULT nextval('public."makeReports_department_id_seq"'::regclass);


--
-- Name: makeReports_gradedrubric id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."makeReports_gradedrubric" ALTER COLUMN id SET DEFAULT nextval('public."makeReports_gradedrubric_id_seq"'::regclass);


--
-- Name: makeReports_gradedrubricitem id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."makeReports_gradedrubricitem" ALTER COLUMN id SET DEFAULT nextval('public."makeReports_gradedrubricitem_id_seq"'::regclass);


--
-- Name: makeReports_gradgoal id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."makeReports_gradgoal" ALTER COLUMN id SET DEFAULT nextval('public."makeReports_gradgoal_id_seq"'::regclass);


--
-- Name: makeReports_graph id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."makeReports_graph" ALTER COLUMN id SET DEFAULT nextval('public."makeReports_graph_id_seq"'::regclass);


--
-- Name: makeReports_profile id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."makeReports_profile" ALTER COLUMN id SET DEFAULT nextval('public."makeReports_profile_id_seq"'::regclass);


--
-- Name: makeReports_report id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."makeReports_report" ALTER COLUMN id SET DEFAULT nextval('public."makeReports_report_id_seq"'::regclass);


--
-- Name: makeReports_reportsupplement id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."makeReports_reportsupplement" ALTER COLUMN id SET DEFAULT nextval('public."makeReports_reportsupplement_id_seq"'::regclass);


--
-- Name: makeReports_requiredfieldsetting id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."makeReports_requiredfieldsetting" ALTER COLUMN id SET DEFAULT nextval('public."makeReports_requiredfieldsetting_id_seq"'::regclass);


--
-- Name: makeReports_resultcommunicate id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."makeReports_resultcommunicate" ALTER COLUMN id SET DEFAULT nextval('public."makeReports_resultcommunicate_id_seq"'::regclass);


--
-- Name: makeReports_rubric id; Type: DEFAULT; Schema: public; Owner: postgres

ALTER TABLE ONLY public."makeReports_rubric" ALTER COLUMN id SET DEFAULT nextval('public."makeReports_rubric_id_seq"'::regclass);


--
-- Name: makeReports_rubricitem id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."makeReports_rubricitem" ALTER COLUMN id SET DEFAULT nextval('public."makeReports_rubricitem_id_seq"'::regclass);


--
-- Name: makeReports_slo id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."makeReports_slo" ALTER COLUMN id SET DEFAULT nextval('public."makeReports_slo_id_seq"'::regclass);


--
-- Name: makeReports_slo_gradGoals id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."makeReports_slo_gradGoals" ALTER COLUMN id SET DEFAULT nextval('public."makeReports_slo_gradGoals_id_seq"'::regclass);


--
-- Name: makeReports_sloinreport id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."makeReports_sloinreport" ALTER COLUMN id SET DEFAULT nextval('public."makeReports_sloinreport_id_seq"'::regclass);


--
-- Name: makeReports_slostatus id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."makeReports_slostatus" ALTER COLUMN id SET DEFAULT nextval('public."makeReports_slostatus_id_seq"'::regclass);


--
-- Name: makeReports_slostostakeholder id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."makeReports_slostostakeholder" ALTER COLUMN id SET DEFAULT nextval('public."makeReports_slostostakeholder_id_seq"'::regclass);




--
-- Name: auth_group auth_group_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group
    ADD CONSTRAINT auth_group_name_key UNIQUE (name);


--
-- Name: auth_group_permissions auth_group_permissions_group_id_permission_id_0cd325b0_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_permission_id_0cd325b0_uniq UNIQUE (group_id, permission_id);


--
-- Name: auth_group_permissions auth_group_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_pkey PRIMARY KEY (id);


--
-- Name: auth_group auth_group_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group
    ADD CONSTRAINT auth_group_pkey PRIMARY KEY (id);


--
-- Name: auth_permission auth_permission_content_type_id_codename_01ab375a_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_codename_01ab375a_uniq UNIQUE (content_type_id, codename);


--
-- Name: auth_permission auth_permission_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_pkey PRIMARY KEY (id);


--
-- Name: auth_user_groups auth_user_groups_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_pkey PRIMARY KEY (id);


--
-- Name: auth_user_groups auth_user_groups_user_id_group_id_94350c0c_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_user_id_group_id_94350c0c_uniq UNIQUE (user_id, group_id);


--
-- Name: auth_user auth_user_pkey; Type: CONSTRAINT; Schema: public; Owner: doadmin
--postgres

ALTER TABLE ONLY public.auth_user
    ADD CONSTRAINT auth_user_pkey PRIMARY KEY (id);


--
-- Name: auth_user_user_permissions auth_user_user_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_pkey PRIMARY KEY (id);


--
-- Name: auth_user_user_permissions auth_user_user_permissions_user_id_permission_id_14a6b632_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_user_id_permission_id_14a6b632_uniq UNIQUE (user_id, permission_id);


--
-- Name: auth_user auth_user_username_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_user
    ADD CONSTRAINT auth_user_username_key UNIQUE (username);


--
-- Name: makeReports_announcement makeReports_announcement_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."makeReports_announcement"
    ADD CONSTRAINT "makeReports_announcement_pkey" PRIMARY KEY (id);


--
-- Name: makeReports_assessment makeReports_assessment_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."makeReports_assessment"
    ADD CONSTRAINT "makeReports_assessment_pkey" PRIMARY KEY (id);


--
-- Name: makeReports_assessmentaggregate makeReports_assessmentaggregate_assessmentVersion_id_key; Type: CONSTRAINT; Schema: public; Owner: doadmin
--

ALTER TABLE ONLY public."makeReports_assessmentaggregate"
    ADD CONSTRAINT "makeReports_assessmentaggregate_assessmentVersion_id_key" UNIQUE ("assessmentVersion_id");


--
-- Name: makeReports_assessmentaggregate makeReports_assessmentaggregate_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."makeReports_assessmentaggregate"
    ADD CONSTRAINT "makeReports_assessmentaggregate_pkey" PRIMARY KEY (id);


--
-- Name: makeReports_assessmentdata makeReports_assessmentdata_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."makeReports_assessmentdata"
    ADD CONSTRAINT "makeReports_assessmentdata_pkey" PRIMARY KEY (id);


--
-- Name: makeReports_assessmentsupplement makeReports_assessmentsupplement_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."makeReports_assessmentsupplement"
    ADD CONSTRAINT "makeReports_assessmentsupplement_pkey" PRIMARY KEY (id);


--
-- Name: makeReports_assessmentversion_supplements makeReports_assessmentve_assessmentversion_id_ass_6b09c182_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."makeReports_assessmentversion_supplements"
    ADD CONSTRAINT "makeReports_assessmentve_assessmentversion_id_ass_6b09c182_uniq" UNIQUE (assessmentversion_id, assessmentsupplement_id);


--
-- Name: makeReports_assessmentversion makeReports_assessmentversion_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."makeReports_assessmentversion"
    ADD CONSTRAINT "makeReports_assessmentversion_pkey" PRIMARY KEY (id);


--
-- Name: makeReports_assessmentversion_supplements makeReports_assessmentversion_supplements_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."makeReports_assessmentversion_supplements"
    ADD CONSTRAINT "makeReports_assessmentversion_supplements_pkey" PRIMARY KEY (id);


--
-- Name: makeReports_college makeReports_college_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."makeReports_college"
    ADD CONSTRAINT "makeReports_college_pkey" PRIMARY KEY (id);


--
-- Name: makeReports_dataadditionalinformation makeReports_dataadditionalinformation_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."makeReports_dataadditionalinformation"
    ADD CONSTRAINT "makeReports_dataadditionalinformation_pkey" PRIMARY KEY (id);


--
-- Name: makeReports_decisionsactions makeReports_decisionsactions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."makeReports_decisionsactions"
    ADD CONSTRAINT "makeReports_decisionsactions_pkey" PRIMARY KEY (id);


--
-- Name: makeReports_decisionsactions makeReports_decisionsactions_sloIR_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."makeReports_decisionsactions"
    ADD CONSTRAINT "makeReports_decisionsactions_sloIR_id_key" UNIQUE ("sloIR_id");


--
-- Name: makeReports_degreeprogram makeReports_degreeprogram_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."makeReports_degreeprogram"
    ADD CONSTRAINT "makeReports_degreeprogram_pkey" PRIMARY KEY (id);


--
-- Name: makeReports_department makeReports_department_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."makeReports_department"
    ADD CONSTRAINT "makeReports_department_pkey" PRIMARY KEY (id);


--
-- Name: makeReports_gradedrubric makeReports_gradedrubric_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."makeReports_gradedrubric"
    ADD CONSTRAINT "makeReports_gradedrubric_pkey" PRIMARY KEY (id);


--
-- Name: makeReports_gradedrubricitem makeReports_gradedrubricitem_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."makeReports_gradedrubricitem"
    ADD CONSTRAINT "makeReports_gradedrubricitem_pkey" PRIMARY KEY (id);


--
-- Name: makeReports_gradgoal makeReports_gradgoal_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."makeReports_gradgoal"
    ADD CONSTRAINT "makeReports_gradgoal_pkey" PRIMARY KEY (id);


--
-- Name: makeReports_graph makeReports_graph_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."makeReports_graph"
    ADD CONSTRAINT "makeReports_graph_pkey" PRIMARY KEY (id);


--
-- Name: makeReports_profile makeReports_profile_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."makeReports_profile"
    ADD CONSTRAINT "makeReports_profile_pkey" PRIMARY KEY (id);


--
-- Name: makeReports_profile makeReports_profile_user_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."makeReports_profile"
    ADD CONSTRAINT "makeReports_profile_user_id_key" UNIQUE (user_id);


--
-- Name: makeReports_report makeReports_report_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."makeReports_report"
    ADD CONSTRAINT "makeReports_report_pkey" PRIMARY KEY (id);


--
-- Name: makeReports_report makeReports_report_rubric_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."makeReports_report"
    ADD CONSTRAINT "makeReports_report_rubric_id_key" UNIQUE (rubric_id);


--
-- Name: makeReports_reportsupplement makeReports_reportsupplement_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."makeReports_reportsupplement"
    ADD CONSTRAINT "makeReports_reportsupplement_pkey" PRIMARY KEY (id);


--
-- Name: makeReports_requiredfieldsetting makeReports_requiredfieldsetting_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."makeReports_requiredfieldsetting"
    ADD CONSTRAINT "makeReports_requiredfieldsetting_pkey" PRIMARY KEY (id);


--
-- Name: makeReports_resultcommunicate makeReports_resultcommunicate_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."makeReports_resultcommunicate"
    ADD CONSTRAINT "makeReports_resultcommunicate_pkey" PRIMARY KEY (id);


--
-- Name: makeReports_rubric makeReports_rubric_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."makeReports_rubric"
    ADD CONSTRAINT "makeReports_rubric_pkey" PRIMARY KEY (id);


--
-- Name: makeReports_rubricitem makeReports_rubricitem_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."makeReports_rubricitem"
    ADD CONSTRAINT "makeReports_rubricitem_pkey" PRIMARY KEY (id);


--
-- Name: makeReports_slo_gradGoals makeReports_slo_gradGoals_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."makeReports_slo_gradGoals"
    ADD CONSTRAINT "makeReports_slo_gradGoals_pkey" PRIMARY KEY (id);


--
-- Name: makeReports_slo_gradGoals makeReports_slo_gradGoals_slo_id_gradgoal_id_00fca829_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."makeReports_slo_gradGoals"
    ADD CONSTRAINT "makeReports_slo_gradGoals_slo_id_gradgoal_id_00fca829_uniq" UNIQUE (slo_id, gradgoal_id);


--
-- Name: makeReports_slo makeReports_slo_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."makeReports_slo"
    ADD CONSTRAINT "makeReports_slo_pkey" PRIMARY KEY (id);


--
-- Name: makeReports_sloinreport makeReports_sloinreport_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."makeReports_sloinreport"
    ADD CONSTRAINT "makeReports_sloinreport_pkey" PRIMARY KEY (id);


--
-- Name: makeReports_slostatus makeReports_slostatus_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."makeReports_slostatus"
    ADD CONSTRAINT "makeReports_slostatus_pkey" PRIMARY KEY (id);


--
-- Name: makeReports_slostatus makeReports_slostatus_sloIR_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."makeReports_slostatus"
    ADD CONSTRAINT "makeReports_slostatus_sloIR_id_key" UNIQUE ("sloIR_id");


--
-- Name: makeReports_slostostakeholder makeReports_slostostakeholder_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."makeReports_slostostakeholder"
    ADD CONSTRAINT "makeReports_slostostakeholder_pkey" PRIMARY KEY (id);


--
-- Name: auth_group_name_a6ea08ec_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_group_name_a6ea08ec_like ON public.auth_group USING btree (name varchar_pattern_ops);


--
-- Name: auth_group_permissions_group_id_b120cbf9; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_group_permissions_group_id_b120cbf9 ON public.auth_group_permissions USING btree (group_id);


--
-- Name: auth_group_permissions_permission_id_84c5c92e; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_group_permissions_permission_id_84c5c92e ON public.auth_group_permissions USING btree (permission_id);


--
-- Name: auth_permission_content_type_id_2f476e4b; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_permission_content_type_id_2f476e4b ON public.auth_permission USING btree (content_type_id);


--
-- Name: auth_user_groups_group_id_97559544; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_user_groups_group_id_97559544 ON public.auth_user_groups USING btree (group_id);


--
-- Name: auth_user_groups_user_id_6a12ed8b; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_user_groups_user_id_6a12ed8b ON public.auth_user_groups USING btree (user_id);


--
-- Name: auth_user_user_permissions_permission_id_1fbb5f2c; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_user_user_permissions_permission_id_1fbb5f2c ON public.auth_user_user_permissions USING btree (permission_id);


--
-- Name: auth_user_user_permissions_user_id_a95ead1b; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_user_user_permissions_user_id_a95ead1b ON public.auth_user_user_permissions USING btree (user_id);


--
-- Name: auth_user_username_6821ab7c_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_user_username_6821ab7c_like ON public.auth_user USING btree (username varchar_pattern_ops);


--
-- Name: makeReports_assessmentdata_assessmentVersion_id_f0247a59; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "makeReports_assessmentdata_assessmentVersion_id_f0247a59" ON public."makeReports_assessmentdata" USING btree ("assessmentVersion_id");


--
-- Name: makeReports_assessmentvers_assessmentsupplement_id_9a30487e; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "makeReports_assessmentvers_assessmentsupplement_id_9a30487e" ON public."makeReports_assessmentversion_supplements" USING btree (assessmentsupplement_id);


--
-- Name: makeReports_assessmentvers_assessmentversion_id_549998a2; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "makeReports_assessmentvers_assessmentversion_id_549998a2" ON public."makeReports_assessmentversion_supplements" USING btree (assessmentversion_id);


--
-- Name: makeReports_assessmentversion_assessment_id_da1cec27; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "makeReports_assessmentversion_assessment_id_da1cec27" ON public."makeReports_assessmentversion" USING btree (assessment_id);


--
-- Name: makeReports_assessmentversion_report_id_2781c22d; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "makeReports_assessmentversion_report_id_2781c22d" ON public."makeReports_assessmentversion" USING btree (report_id);


--
-- Name: makeReports_assessmentversion_slo_id_70157d4a; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "makeReports_assessmentversion_slo_id_70157d4a" ON public."makeReports_assessmentversion" USING btree (slo_id);


--
-- Name: makeReports_dataadditionalinformation_report_id_d9926511; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "makeReports_dataadditionalinformation_report_id_d9926511" ON public."makeReports_dataadditionalinformation" USING btree (report_id);


--
-- Name: makeReports_degreeprogram_department_id_9d22e7bc; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "makeReports_degreeprogram_department_id_9d22e7bc" ON public."makeReports_degreeprogram" USING btree (department_id);


--
-- Name: makeReports_department_college_id_c34c69b5; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "makeReports_department_college_id_c34c69b5" ON public."makeReports_department" USING btree (college_id);


--
-- Name: makeReports_gradedrubric_rubricVersion_id_8138acbd; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "makeReports_gradedrubric_rubricVersion_id_8138acbd" ON public."makeReports_gradedrubric" USING btree ("rubricVersion_id");


--
-- Name: makeReports_gradedrubricitem_item_id_8800f750; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "makeReports_gradedrubricitem_item_id_8800f750" ON public."makeReports_gradedrubricitem" USING btree (item_id);


--
-- Name: makeReports_gradedrubricitem_rubric_id_9259d933; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "makeReports_gradedrubricitem_rubric_id_9259d933" ON public."makeReports_gradedrubricitem" USING btree (rubric_id);


--
-- Name: makeReports_profile_department_id_50419a58; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "makeReports_profile_department_id_50419a58" ON public."makeReports_profile" USING btree (department_id);


--
-- Name: makeReports_report_degreeProgram_id_9699ef2c; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "makeReports_report_degreeProgram_id_9699ef2c" ON public."makeReports_report" USING btree ("degreeProgram_id");


--
-- Name: makeReports_reportsupplement_report_id_a170118a; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "makeReports_reportsupplement_report_id_a170118a" ON public."makeReports_reportsupplement" USING btree (report_id);


--
-- Name: makeReports_resultcommunicate_report_id_7df2cee4; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "makeReports_resultcommunicate_report_id_7df2cee4" ON public."makeReports_resultcommunicate" USING btree (report_id);


--
-- Name: makeReports_rubricitem_rubricVersion_id_6c8ebffc; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "makeReports_rubricitem_rubricVersion_id_6c8ebffc" ON public."makeReports_rubricitem" USING btree ("rubricVersion_id");


--
-- Name: makeReports_slo_gradGoals_gradgoal_id_3fb61203; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "makeReports_slo_gradGoals_gradgoal_id_3fb61203" ON public."makeReports_slo_gradGoals" USING btree (gradgoal_id);


--
-- Name: makeReports_slo_gradGoals_slo_id_294858df; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "makeReports_slo_gradGoals_slo_id_294858df" ON public."makeReports_slo_gradGoals" USING btree (slo_id);


--
-- Name: makeReports_sloinreport_report_id_8e936775; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "makeReports_sloinreport_report_id_8e936775" ON public."makeReports_sloinreport" USING btree (report_id);


--
-- Name: makeReports_sloinreport_slo_id_16991708; Type: INDEX; Schema: public; Owner: doadmin
--postgres

CREATE INDEX "makeReports_sloinreport_slo_id_16991708" ON public."makeReports_sloinreport" USING btree (slo_id);


--
-- Name: makeReports_slostostakeholder_report_id_20c5bb85; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "makeReports_slostostakeholder_report_id_20c5bb85" ON public."makeReports_slostostakeholder" USING btree (report_id);


--
-- Name: auth_group_permissions auth_group_permissio_permission_id_84c5c92e_fk_auth_perm; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissio_permission_id_84c5c92e_fk_auth_perm FOREIGN KEY (permission_id) REFERENCES public.auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_group_permissions auth_group_permissions_group_id_b120cbf9_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_b120cbf9_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES public.auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_permission auth_permission_content_type_id_2f476e4b_fk_django_co; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_2f476e4b_fk_django_co FOREIGN KEY (content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_groups auth_user_groups_group_id_97559544_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_group_id_97559544_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES public.auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_groups auth_user_groups_user_id_6a12ed8b_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: doadmin
--

ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_user_id_6a12ed8b_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_user_permissions auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm FOREIGN KEY (permission_id) REFERENCES public.auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_user_permissions auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;




--
-- Name: makeReports_assessmentaggregate makeReports_assessme_assessmentVersion_id_1c134dc4_fk_makeRepor; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."makeReports_assessmentaggregate"
    ADD CONSTRAINT "makeReports_assessme_assessmentVersion_id_1c134dc4_fk_makeRepor" FOREIGN KEY ("assessmentVersion_id") REFERENCES public."makeReports_assessmentversion"(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: makeReports_assessmentdata makeReports_assessme_assessmentVersion_id_f0247a59_fk_makeRepor; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."makeReports_assessmentdata"
    ADD CONSTRAINT "makeReports_assessme_assessmentVersion_id_f0247a59_fk_makeRepor" FOREIGN KEY ("assessmentVersion_id") REFERENCES public."makeReports_assessmentversion"(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: makeReports_assessmentversion makeReports_assessme_assessment_id_da1cec27_fk_makeRepor; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."makeReports_assessmentversion"
    ADD CONSTRAINT "makeReports_assessme_assessment_id_da1cec27_fk_makeRepor" FOREIGN KEY (assessment_id) REFERENCES public."makeReports_assessment"(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: makeReports_assessmentversion_supplements makeReports_assessme_assessmentsupplement_9a30487e_fk_makeRepor; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."makeReports_assessmentversion_supplements"
    ADD CONSTRAINT "makeReports_assessme_assessmentsupplement_9a30487e_fk_makeRepor" FOREIGN KEY (assessmentsupplement_id) REFERENCES public."makeReports_assessmentsupplement"(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: makeReports_assessmentversion_supplements makeReports_assessme_assessmentversion_id_549998a2_fk_makeRepor; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."makeReports_assessmentversion_supplements"
    ADD CONSTRAINT "makeReports_assessme_assessmentversion_id_549998a2_fk_makeRepor" FOREIGN KEY (assessmentversion_id) REFERENCES public."makeReports_assessmentversion"(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: makeReports_assessmentversion makeReports_assessme_report_id_2781c22d_fk_makeRepor; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."makeReports_assessmentversion"
    ADD CONSTRAINT "makeReports_assessme_report_id_2781c22d_fk_makeRepor" FOREIGN KEY (report_id) REFERENCES public."makeReports_report"(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: makeReports_assessmentversion makeReports_assessme_slo_id_70157d4a_fk_makeRepor; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."makeReports_assessmentversion"
    ADD CONSTRAINT "makeReports_assessme_slo_id_70157d4a_fk_makeRepor" FOREIGN KEY (slo_id) REFERENCES public."makeReports_sloinreport"(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: makeReports_dataadditionalinformation makeReports_dataaddi_report_id_d9926511_fk_makeRepor; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."makeReports_dataadditionalinformation"
    ADD CONSTRAINT "makeReports_dataaddi_report_id_d9926511_fk_makeRepor" FOREIGN KEY (report_id) REFERENCES public."makeReports_report"(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: makeReports_decisionsactions makeReports_decision_sloIR_id_753a91d7_fk_makeRepor; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."makeReports_decisionsactions"
    ADD CONSTRAINT "makeReports_decision_sloIR_id_753a91d7_fk_makeRepor" FOREIGN KEY ("sloIR_id") REFERENCES public."makeReports_sloinreport"(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: makeReports_degreeprogram makeReports_degreepr_department_id_9d22e7bc_fk_makeRepor; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."makeReports_degreeprogram"
    ADD CONSTRAINT "makeReports_degreepr_department_id_9d22e7bc_fk_makeRepor" FOREIGN KEY (department_id) REFERENCES public."makeReports_department"(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: makeReports_department makeReports_departme_college_id_c34c69b5_fk_makeRepor; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."makeReports_department"
    ADD CONSTRAINT "makeReports_departme_college_id_c34c69b5_fk_makeRepor" FOREIGN KEY (college_id) REFERENCES public."makeReports_college"(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: makeReports_gradedrubricitem makeReports_gradedru_item_id_8800f750_fk_makeRepor; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."makeReports_gradedrubricitem"
    ADD CONSTRAINT "makeReports_gradedru_item_id_8800f750_fk_makeRepor" FOREIGN KEY (item_id) REFERENCES public."makeReports_rubricitem"(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: makeReports_gradedrubric makeReports_gradedru_rubricVersion_id_8138acbd_fk_makeRepor; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."makeReports_gradedrubric"
    ADD CONSTRAINT "makeReports_gradedru_rubricVersion_id_8138acbd_fk_makeRepor" FOREIGN KEY ("rubricVersion_id") REFERENCES public."makeReports_rubric"(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: makeReports_gradedrubricitem makeReports_gradedru_rubric_id_9259d933_fk_makeRepor; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."makeReports_gradedrubricitem"
    ADD CONSTRAINT "makeReports_gradedru_rubric_id_9259d933_fk_makeRepor" FOREIGN KEY (rubric_id) REFERENCES public."makeReports_gradedrubric"(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: makeReports_profile makeReports_profile_department_id_50419a58_fk_makeRepor; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."makeReports_profile"
    ADD CONSTRAINT "makeReports_profile_department_id_50419a58_fk_makeRepor" FOREIGN KEY (department_id) REFERENCES public."makeReports_department"(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: makeReports_profile makeReports_profile_user_id_522878ba_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."makeReports_profile"
    ADD CONSTRAINT "makeReports_profile_user_id_522878ba_fk_auth_user_id" FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: makeReports_report makeReports_report_degreeProgram_id_9699ef2c_fk_makeRepor; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."makeReports_report"
    ADD CONSTRAINT "makeReports_report_degreeProgram_id_9699ef2c_fk_makeRepor" FOREIGN KEY ("degreeProgram_id") REFERENCES public."makeReports_degreeprogram"(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: makeReports_report makeReports_report_rubric_id_f25148ee_fk_makeRepor; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."makeReports_report"
    ADD CONSTRAINT "makeReports_report_rubric_id_f25148ee_fk_makeRepor" FOREIGN KEY (rubric_id) REFERENCES public."makeReports_gradedrubric"(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: makeReports_reportsupplement makeReports_reportsu_report_id_a170118a_fk_makeRepor; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."makeReports_reportsupplement"
    ADD CONSTRAINT "makeReports_reportsu_report_id_a170118a_fk_makeRepor" FOREIGN KEY (report_id) REFERENCES public."makeReports_report"(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: makeReports_resultcommunicate makeReports_resultco_report_id_7df2cee4_fk_makeRepor; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."makeReports_resultcommunicate"
    ADD CONSTRAINT "makeReports_resultco_report_id_7df2cee4_fk_makeRepor" FOREIGN KEY (report_id) REFERENCES public."makeReports_report"(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: makeReports_rubricitem makeReports_rubricit_rubricVersion_id_6c8ebffc_fk_makeRepor; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."makeReports_rubricitem"
    ADD CONSTRAINT "makeReports_rubricit_rubricVersion_id_6c8ebffc_fk_makeRepor" FOREIGN KEY ("rubricVersion_id") REFERENCES public."makeReports_rubric"(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: makeReports_slo_gradGoals makeReports_slo_gradGoals_slo_id_294858df_fk_makeReports_slo_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."makeReports_slo_gradGoals"
    ADD CONSTRAINT "makeReports_slo_gradGoals_slo_id_294858df_fk_makeReports_slo_id" FOREIGN KEY (slo_id) REFERENCES public."makeReports_slo"(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: makeReports_slo_gradGoals makeReports_slo_grad_gradgoal_id_3fb61203_fk_makeRepor; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."makeReports_slo_gradGoals"
    ADD CONSTRAINT "makeReports_slo_grad_gradgoal_id_3fb61203_fk_makeRepor" FOREIGN KEY (gradgoal_id) REFERENCES public."makeReports_gradgoal"(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: makeReports_sloinreport makeReports_sloinrep_report_id_8e936775_fk_makeRepor; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."makeReports_sloinreport"
    ADD CONSTRAINT "makeReports_sloinrep_report_id_8e936775_fk_makeRepor" FOREIGN KEY (report_id) REFERENCES public."makeReports_report"(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: makeReports_sloinreport makeReports_sloinreport_slo_id_16991708_fk_makeReports_slo_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."makeReports_sloinreport"
    ADD CONSTRAINT "makeReports_sloinreport_slo_id_16991708_fk_makeReports_slo_id" FOREIGN KEY (slo_id) REFERENCES public."makeReports_slo"(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: makeReports_slostatus makeReports_slostatu_sloIR_id_6a781077_fk_makeRepor; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."makeReports_slostatus"
    ADD CONSTRAINT "makeReports_slostatu_sloIR_id_6a781077_fk_makeRepor" FOREIGN KEY ("sloIR_id") REFERENCES public."makeReports_sloinreport"(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: makeReports_slostostakeholder makeReports_slostost_report_id_20c5bb85_fk_makeRepor; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."makeReports_slostostakeholder"
    ADD CONSTRAINT "makeReports_slostost_report_id_20c5bb85_fk_makeRepor" FOREIGN KEY (report_id) REFERENCES public."makeReports_report"(id) DEFERRABLE INITIALLY DEFERRED;


--
-- PostgreSQL database dump complete
--


