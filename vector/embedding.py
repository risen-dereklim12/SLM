import ollama
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vector.client import VectorClient
from qdrant_client.models import Distance, VectorParams, PointStruct, Filter, FieldCondition, MatchValue
from dotenv import dotenv_values

config = dotenv_values(".env")

documents = [
    {
        "text": "Personal Data Protection Act 2012 2020 REVISED EDITION This revised edition incorporates all amendments up to and including 1 December 2021 and comes into operation on 31 December 2021",
        "section": "Title",
        "source": "PDPA 2012 (2020 Rev Edition)",
        "effective_date": "31-12-2021"
    },
    {
        "text": "An Act to govern the collection, use and disclosure of personal data by organisations, and to establish the Do Not Call Register and to provide for its administration, and for matters connected therewith.",
        "section": "Purpose",
        "source": "PDPA 2012 (2020 Rev Edition)",
        "effective_date": "31-12-2021"
    },
    {
        "text": "2 January 2013: Parts I, II, VIII, IX (except sections 36 to 38, 41 and 43 to 48) and X (except section 67(1)), and the First, Seventh and Ninth Schedules ; 2 December 2013: Sections 36, 37, 38 and 41 ; 2 January 2014: Sections 43 to 48 and 67(1) and the Eighth Schedule ; 2 July 2014: Parts III to VII, and the Second to Sixth Schedules ",
        "section": "Revisions History",
        "source": "PDPA 2012 (2020 Rev Edition)",
        "effective_date": "31-12-2021"
    },
    {
        "text": "1.  This Act is the Personal Data Protection Act 2012.",
        "section": "Short title",
        "source": "PDPA 2012 (2020 Rev Edition)",
        "effective_date": "31-12-2021"
    },
    {
        "text": '''"advisory committee" means an advisory committee appointed under section 7; "Appeal Committee" means a Data Protection Appeal Committee constituted under section 48P(4), read with the Seventh Schedule; "Appeal Panel" means the Data Protection Appeal Panel established by section 48P(1); "authorised officer", in relation to the exercise of any power or performance of any function or duty under any provision of this Act, means a person to whom the exercise of that power or performance of that function or duty under that provision has been delegated under section 38 of the Info‑communications Media Development Authority Act 2016; "Authority" means the Info‑communications Media Development Authority established by section 3 of the Info‑communications Media Development Authority Act 2016;''',
        "section": "Interpretation",
        "source": "PDPA 2012 (2020 Rev Edition)",
        "effective_date": "31-12-2021"
    },
    {
        "text": '''"benefit plan" means an insurance policy, a pension plan, an annuity, a provident fund plan or other similar plan; "business" includes the activity of any organisation, whether or not carried on for purposes of gain, or conducted on a regular, repetitive or continuous basis, but does not include an individual acting in his or her personal or domestic capacity; "business contact information" means an individual's name, position name or title, business telephone number, business address, business electronic mail address or business fax number and any other similar information about the individual, not provided by the individual solely for his or her personal purposes; "Chief Executive", in relation to the Authority, means the Chief Executive of the Authority appointed under section 40(2) of the Info‑communications Media Development Authority Act 2016, and includes any individual acting in that capacity; "Commission" means the person designated as the Personal Data Protection Commission under section 5 to be responsible for the administration of this Act; "Commissioner" means the Commissioner for Personal Data Protection appointed under section 8(1)(a), and includes any Deputy Commissioner for Personal Data Protection or Assistant Commissioner for Personal Data Protection appointed under section 8(1)(b);''',
        "section": "Interpretation",
        "source": "PDPA 2012 (2020 Rev Edition)",
        "effective_date": "31-12-2021"
    },
    {
        "text": '''"credit bureau" means an organisation which — (a) provides credit reports for gain or profit; or (b) provides credit reports on a routine, non‑profit basis as an ancillary part of a business carried on for gain or profit; "credit report" means a communication, whether in written, oral or other form, provided to an organisation to assess the creditworthiness of an individual in relation to a transaction between the organisation and the individual; "data intermediary" means an organisation which processes personal data on behalf of another organisation but does not include an employee of that other organisation;''',
         "section": "Interpretation",
        "source": "PDPA 2012 (2020 Rev Edition)",
        "effective_date": "31-12-2021"
    },
    {
        "text": '''"derived personal data" — (a) means personal data about an individual that is derived by an organisation in the course of business from other personal data, about the individual or another individual, in the possession or under the control of the organisation; but (b) does not include personal data derived by the organisation using any prescribed means or method; "document" includes information recorded in any form; "domestic" means related to home or family; "education institution" means an organisation that provides education, including instruction, training or teaching, whether by itself or in association or collaboration with, or by affiliation with, any other person;''',
        "section": "Interpretation",
        "source": "PDPA 2012 (2020 Rev Edition)",
        "effective_date": "31-12-2021"
    },
    {
        "text": '''"employee" includes a volunteer; "employment" includes working under an unpaid volunteer work relationship; "evaluative purpose" means — (a) the purpose of determining the suitability, eligibility or qualifications of the individual to whom the data relates — (i) for employment or for appointment to office; (ii) for promotion in employment or office or for continuance in employment or office; (iii) for removal from employment or office; (iv) for admission to an education institution; (v) for the awarding of contracts, awards, bursaries, scholarships, honours or other similar benefits; (vi) for selection for an athletic or artistic purpose; or (vii) for grant of financial or social assistance, or the delivery of appropriate health services, under any scheme administered by a public agency;''',
        "section": "Interpretation",
        "source": "PDPA 2012 (2020 Rev Edition)",
        "effective_date": "31-12-2021"
    },
    {
        "text": '''(b) the purpose of determining whether any contract, award, bursary, scholarship, honour or other similar benefit should be continued, modified or cancelled; (c) the purpose of deciding whether to insure any individual or property or to continue or renew the insurance of any individual or property; or (d) such other similar purposes as the Minister may prescribe; "individual" means a natural person, whether living or deceased; "inspector" means an individual appointed as an inspector under section 8(1)(b); "investigation" means an investigation relating to — (a) a breach of an agreement; (b) a contravention of any written law, or any rule of professional conduct or other requirement imposed by any regulatory authority in exercise of its powers under any written law; or (c) a circumstance or conduct that may result in a remedy or relief being available under any law; "national interest" includes national defence, national security, public security, the maintenance of essential services and the conduct of international affairs;''',
        "section": "Interpretation",
        "source": "PDPA 2012 (2020 Rev Edition)",
        "effective_date": "31-12-2021"
    },
    {
        "text": '''"organisation" includes any individual, company, association or body of persons, corporate or unincorporated, whether or not — (a) formed or recognised under the law of Singapore; or (b) resident, or having an office or a place of business, in Singapore; "personal data" means data, whether true or not, about an individual who can be identified — (a) from that data; or (b) from that data and other information to which the organisation has or is likely to have access; "prescribed healthcare body" means a healthcare body prescribed for the purposes of the Second Schedule by the Minister charged with the responsibility for health;''',
        "section": "Interpretation",
        "source": "PDPA 2012 (2020 Rev Edition)",
        "effective_date": "31-12-2021"
    },
    {
        "text": '''"prescribed law enforcement agency" means an authority charged with the duty of investigating offences or charging offenders under written law, prescribed for the purposes of sections 21(4) and 26D(6) and the Second Schedule by the Minister charged with the responsibility for that authority; "private trust" means a trust for the benefit of one or more designated individuals who are the settlor's friends or family members;''',
        "section": "Interpretation",
        "source": "PDPA 2012 (2020 Rev Edition)",
        "effective_date": "31-12-2021"
    },
    {
        "text": '''"proceedings" means any civil, criminal or administrative proceedings by or before a court, tribunal or regulatory authority that is related to the allegation of — (a) a breach of an agreement; (b) a contravention of any written law or any rule of professional conduct or other requirement imposed by any regulatory authority in exercise of its powers under any written law; or (c) a wrong or a breach of a duty for which a remedy is claimed under any law; "processing", in relation to personal data, means the carrying out of any operation or set of operations in relation to the personal data, and includes any of the following: (a) recording; (b) holding; (c) organisation, adaptation or alteration; (d) retrieval; (e) combination; (f) transmission; (g) erasure or destruction;''',
        "section": "Interpretation",
        "source": "PDPA 2012 (2020 Rev Edition)",
        "effective_date": "31-12-2021"
    },
    {
        "text": '''"public agency" includes — (a) the Government, including any ministry, department, agency, or organ of State; (b) any tribunal appointed under any written law; or (c) any statutory body specified under subsection (2); "publicly available", in relation to personal data about an individual, means personal data that is generally available to the public, and includes personal data which can be observed by reasonably expected means at a location or an event — (a) at which the individual appears; and (b) that is open to the public;''',
        "section": "Interpretation",
        "source": "PDPA 2012 (2020 Rev Edition)",
        "effective_date": "31-12-2021"
    },
    {
        "text": '''"relevant body" means the Commission, the Appeal Panel or any Appeal Committee; "tribunal" includes a judicial or quasi‑judicial body or a disciplinary, an arbitral or a mediatory body; "user activity data", in relation to an organisation, means personal data about an individual that is created in the course or as a result of the individual's use of any product or service provided by the organisation; "user‑provided data", in relation to an organisation, means personal data provided by an individual to the organisation.''',
        "section": "Interpretation",
        "source": "PDPA 2012 (2020 Rev Edition)",
        "effective_date": "31-12-2021"
    },
    {
        "text": '''(2) The Minister may, by notification in the Gazette, specify any statutory body established under a public Act for a public function to be a public agency for the purposes of this Act. Purpose 3. The purpose of this Act is to govern the collection, use and disclosure of personal data by organisations in a manner that recognises both the right of individuals to protect their personal data and the need of organisations to collect, use or disclose personal data for purposes that a reasonable person would consider appropriate in the circumstances.''',
        "section": "Interpretation",
        "source": "PDPA 2012 (2020 Rev Edition)",
        "effective_date": "31-12-2021"
    },
    {
        "text": '''Application of Act 4.—(1) Parts 3, 4, 5, 6, 6A and 6B do not impose any obligation on — (a) any individual acting in a personal or domestic capacity; (b) any employee acting in the course of his or her employment with an organisation; (c) any public agency; or (d) any other organisations or personal data, or classes of organisations or personal data, prescribed for the purposes of this provision.''',
        "section": "Interpretation",
        "source": "PDPA 2012 (2020 Rev Edition)",
        "effective_date": "31-12-2021"
    },
    {
        "text": '''[40/2020] (2) Parts 3, 4, 5, 6 (except sections 24 and 25), 6A (except sections 26C(3)(a) and 26E) and 6B do not impose any obligation on a data intermediary in respect of its processing of personal data on behalf of and for the purposes of another organisation pursuant to a contract which is evidenced or made in writing. [40/2020] (3) An organisation has the same obligation under this Act in respect of personal data processed on its behalf and for its purposes by a data intermediary as if the personal data were processed by the organisation itself.''',
        "section": "Interpretation",
        "source": "PDPA 2012 (2020 Rev Edition)",
        "effective_date": "31-12-2021"
    },
    {
        "text": '''(4) This Act does not apply in respect of — (a) personal data about an individual that is contained in a record that has been in existence for at least 100 years; or (b) personal data about a deceased individual, except that the provisions relating to the disclosure of personal data and section 24 (protection of personal data) apply in respect of personal data about an individual who has been dead for 10 years or less. (5) Except where business contact information is expressly mentioned, Parts 3, 4, 5, 6 and 6A do not apply to business contact information.''',
        "section": "Interpretation",
        "source": "PDPA 2012 (2020 Rev Edition)",
        "effective_date": "31-12-2021"
    },
    {
        "text": '''(6) Unless otherwise expressly provided in this Act — (a) nothing in Parts 3, 4, 5, 6, 6A and 6B affects any authority, right, privilege or immunity conferred, or obligation or limitation imposed, by or under the law, including legal privilege, except that the performance of a contractual obligation is not an excuse for contravening this Act; and (b) the provisions of other written law prevail to the extent that any provision of Parts 3, 4, 5, 6, 6A and 6B is inconsistent with the provisions of that other written law.''',
        "section": "Interpretation",
        "source": "PDPA 2012 (2020 Rev Edition)",
        "effective_date": "31-12-2021"
    },
]

class Embedding:
    def __init__(self, model=config['EMBEDDING_MODEL']):
        self.model = model
        self.vector_client = VectorClient("PDPA", 1024, "http://localhost:6333", Distance.DOT)

    def create_collection(self):
        self.vector_client.create_collection()

    def embed(self, documents):
        points = []
        # store each document in a vector embedding database
        for i, d in enumerate(documents):
            response = ollama.embed(model=config['EMBEDDING_MODEL'], input=d["text"])
            vector = response["embeddings"]
            if isinstance(vector[0], list):  # it's a list of lists
                vector = vector[0]
            point = PointStruct(id=i, vector=vector, payload=d)
            points.append(point)
        return points

    def encode(self, input_text):
        response = ollama.embed(model=config['EMBEDDING_MODEL'], input=input_text)
        return response

    def search_vector(self, vector, limit=1):
        search_result = self.vector_client.search(vector, limit=limit)
        return search_result

if __name__ == "__main__":
    embedding = Embedding()
    # points = embedding.embed(documents)
    # # print(points[0])
    # # for p in points:
    # #     operation_info = embedding.vector_client.upsert(points)
    # #     print(operation_info)
    # search_result = embedding.search_vector([-0.0036573352, 0.007857362, 0.035704605, -0.0034508847, 0.045991436, 0.032797985, -0.017289447, -0.06293157, -0.03753654, -0.022535224, -0.037320405, -0.044267893, -0.026862878, -0.04003827, -0.03919297, -0.01614415, 0.007836565, -0.006142959, 0.041159283, -0.07957603, 0.03769638, -0.021716584, -0.0021302893, -0.021463033, 0.009466263, 0.013998661, 0.052006207, 0.027238334, -0.086355984, -0.02766234, 0.046974648, -0.049055245, 0.036518242, 0.03304195, -0.022015886, 0.003958315, -0.027088681, -0.053258847, -0.030072222, -0.018945385, -0.03951759, -0.0065238415, -0.07252855, -0.0061789583, -0.014137303, 0.014238933, -0.042828124, -0.016609093, -0.0038371128, -0.0050943485, -0.0028225824, 0.048020817, -0.005184154, -0.0016996159, -0.016489213, -0.010976336, 0.00626203, -0.09810207, -0.0070286314, -0.0068710297, 0.0844184, -0.04201927, 0.040138055, 0.008047912, 0.04695686, -0.0028259314, -0.008769551, -0.0555976, -0.037312172, -0.056456994, -0.041406404, 0.0008671971, 0.0044090278, 0.018065635, -0.05320839, -0.058472183, 0.05078128, -0.0014977326, 0.05013858, 0.036959555, 0.082896635, -0.06608914, 0.01925566, -0.013949834, 0.0009200447, -0.020946572, -9.3280905e-05, -0.0020516242, 0.0038455022, 0.06713945, 0.03568318, -0.011904117, 0.017541822, 0.0028607685, 0.04133226, -0.04236395, -0.019356256, -0.010834649, 0.031190148, 0.012892774, 0.024386108, 0.004358376, 0.012613618, -0.01109069, -0.0256421, 0.023639811, 0.051652733, 0.003969542, 0.027241265, 0.0059920684, 0.0017061662, -0.026366739, 0.0023208985, 0.014051145, -0.044422884, 0.019614287, 0.00208982, 0.004788739, 0.08525964, 0.044053897, 0.03797219, 0.008575743, 0.059921637, 0.043591376, 0.029767342, 0.023326468, 0.010132225, 0.06690567, -0.027882684, -0.046926823, -0.0010042413, 0.008745506, -0.0003801883, -7.831778e-05, -0.04852621, 0.022684732, -0.049566243, -0.07468052, 0.055804912, -0.033217344, 0.05390072, 0.008348876, 0.04464997, -0.0168811, 0.0027458926, -0.008022565, 0.0075883013, 0.0135920765, -0.037432704, -0.06593928, 0.03322245, 0.03211817, -0.0025365937, -0.02902619, 0.020451827, 0.033057034, 0.022853909, 0.02553504, -0.05615496, -0.019578194, 0.08008065, -0.00046591676, 0.023083115, 0.029613094, 0.06515887, -0.00857911, -0.0095630195, 0.052669924, 0.058822792, -0.009756319, -0.018742187, -0.038549222, 0.07576313, -0.011816911, -0.0021732498, 0.009069998, -0.019082682, 0.017522372, 0.030043138, 0.022984492, -0.026528198, 0.03772258, -0.010528284, 0.009292565, -0.047939815, 0.0052683176, 0.009765408, -0.026975796, 5.3770014e-05, 0.022960333, -0.031181263, -0.019652361, -0.032325063, -0.009395914, -0.013985525, 0.013947964, 0.04520081, 0.00984968, 0.0063431705, 0.088383906, 0.035588954, 0.014264491, 0.07510314, -0.04018166, -0.062410675, -0.007838281, 0.011976628, 0.018730663, 0.0071952427, 0.053464275, -0.028678201, -0.018264208, 0.01517679, -0.019220112, -0.01433364, 0.047329478, -0.021237371, -0.020942885, 0.07037614, 0.008833998, 0.02077367, 0.0034808505, 0.056853235, 0.05059002, 0.028315185, -0.03265907, -0.0030517287, -0.08179443, 0.031283617, -0.031001633, 0.00068936945, -0.06252721, 0.022927687, -0.010723115, 0.005175127, -0.019444643, -0.032320697, -0.025136285, 0.026234992, -0.030600006, 0.011995006, 0.056280293, 0.064909264, 0.0103284065, -0.02068707, 0.05777916, 0.016825384, -0.018299686, 0.018377332, -0.0052482565, 0.0018717718, -0.06163256, 0.0055666836, -0.018873177, 0.00774498, -0.006127281, 0.007395462, 0.016780298, 0.031004531, 0.013032784, -0.05773765, -0.050463147, 0.023353133, 0.01678576, -0.058866072, -0.07322082, -0.01745031, -0.03606395, -0.04306776, -0.000222827, -0.022403615, -0.049472302, -0.009541178, 0.038006674, -0.01578641, 0.012240317, 0.07871186, 0.025333244, -0.021176066, 0.0034853292, 0.03323854, 0.021813828, 0.00607595, 0.027647352, 0.035628647, -0.059322584, 0.028767463, -0.053297974, -0.019867314, -0.024752969, -0.0012653723, -0.012450299, -0.04817436, -0.000578886, 0.054194946, 0.008779473, -0.02397617, 0.078810155, 0.0054411287, 0.013172662, 0.0076064756, -0.05904556, 0.01851035, -0.011567711, -0.01080324, -0.039367925, 0.0038740307, -0.034561895, 0.0039017634, 0.016719887, -0.041762393, -0.027015015, 0.008231657, 0.051904973, 0.053757843, -0.055198606, 0.014800627, -0.011904323, 0.11984956, -0.01509626, 0.06732921, 0.030462423, -0.025229072, 0.00776305, -0.016918462, -0.064722165, 0.0100669535, 0.018270388, 0.057707928, -0.033900633, -0.032223772, -0.017223757, -0.0064107915, 0.01989346, 0.0128798615, -0.041769993, -0.036837764, -0.03951802, -0.011847611, -0.013490987, 0.0129225105, -0.0005386571, -0.02169194, -0.05913847, 0.004773752, 0.077844255, -0.0048474157, -0.08539783, -0.0027671375, 0.039016522, -0.03191851, -0.013886156, 0.015819946, -0.03182071, -0.030648718, -0.041059554, -0.038720135, 0.044657554, 0.025322057, 0.012918553, 0.03802453, -0.024630472, -0.020859817, 0.007488812, -0.047893573, -0.008475871, -0.0034929332, 0.0049031028, 0.017256055, -0.025166027, -0.049974, 0.004904274, -0.00018724811, 0.00024723148, -0.08310332, -0.087586366, 0.021033831, 0.050377008, -0.013875531, -0.040100157, 0.021096071, -0.024165442, -0.039210383, -0.00926722, 0.05090432, 0.056009214, 0.053886265, 0.019493386, 0.007928774, 0.017515998, -7.735487e-06, 0.08414849, -0.03432096, -0.017777164, -0.0036035415, 0.02816197, -0.01510611, -0.07407353, 0.058812454, -0.044639584, 0.015389496, 0.00573101, 0.018401762, 0.015332185, 0.008826891, -0.014518429, -0.03212072, -0.008741514, 0.00846944, -0.06376197, -0.018061915, -0.06461257, 0.03619907, -0.00768225, -0.027730951, 0.038796384, -0.06586333, 0.029603934, 0.036450863, -0.0047607576, -0.010945772, -0.0058517796, 0.005556832, -0.07090303, 0.00690404, 0.036613476, 0.07260642, 0.022592822, -0.009460419, 0.021783821, -0.05072622, 0.03878935, -0.061634976, -0.03322921, -0.0044213263, -0.016383262, 0.02124844, -0.00601826, -0.051555544, 0.0017698868, -0.012014329, 0.004407279, 0.019028816, -0.0039228112, 0.071175106, 0.01199204, -0.00575052, -0.008728642, -0.018974794, 0.004800523, 0.0011602732, 0.0205079, 0.026963493, 0.0018928581, -0.033150297, 0.050875418, 0.046254527, 0.0030091745, 0.033769205, -0.03530241, 0.04411275, -0.016830824, -0.020517373, 0.006732742, 0.062271688, 0.0005982759, -0.010615876, 0.021205015, -0.043157533, -0.007961009, -0.010260703, -0.06432934, 0.01067856, 0.05902515, -0.05987978, 0.0041062157, 0.017802708, -0.026366625, 0.0055607166, -0.012874805, 0.007524366, -0.005806312, 0.0009812854, -0.026630158, -0.05389811, -0.05579818, -0.006952962, 0.026080105, 0.017550698, -0.006166782, -0.04081395, 0.038423713, 0.011474019, 0.013000634, 0.019352539, -0.017297935, 0.028609514, 0.016575351, -0.002152634, -0.003143706, -0.002300399, -0.028626615, -0.010005983, -0.026028292, -0.0029009955, 0.019280879, -0.016092712, -0.04963151, -0.030342843, -0.016797021, -0.022306306, 0.004262189, 0.01585499, -0.024362277, -0.01759839, -0.063784964, -0.060469422, 0.009277008, -0.060944073, -0.031471882, 0.016561652, 0.014087537, -0.033979878, 0.011437147, -0.011540265, 0.008286143, -0.022729456, -0.032668576, 0.051359054, -0.021998191, -0.010342443, -0.016189601, 0.03944481, 0.047487516, 0.007186633, -0.0162702, -0.030193336, -0.024585858, 0.028858863, -0.0023321733, 0.044601023, 0.02335346, 0.00815201, -0.00016448121, -0.025948513, 0.029659512, 0.0071625155, -0.024746574, -0.013291676, 0.04203127, 0.033052392, -0.06682331, -0.017328363, 0.0006414063, 0.050789382, 0.052970037, 0.050220117, 0.037930712, -0.088053785, -0.0013487848, -0.034526773, -0.034628928, 0.070214294, -0.03917753, 0.031320464, -0.02724542, -0.015752094, 0.0013267793, 0.007738947, 0.018161237, 0.02023254, 0.0073828725, 0.0136682615, 0.03778925, -0.021746496, -0.05689842, 0.020037381, -0.014764525, 0.015547686, 0.020244813, -0.0068706353, -0.02726442, -0.01746669, 0.035008077, 0.0323297, 0.011451642, -0.025327379, 0.027240837, 0.06442974, 0.08737209, 0.006897985, 0.021267774, 0.016948562, -0.013382172, 0.013841923, 0.031875983, -0.07997596, -0.07448644, 0.036004916, 0.013325572, -0.10234274, 0.029046614, -0.0058677546, -0.025263906, -0.021748234, 0.016885271, -0.032028258, 0.041919887, 0.06992478, -0.016488671, 0.0630041, 0.012177085, -0.058036067, 0.04714847, 0.07327604, -0.031382035, -0.010812484, 0.00930816, 0.017788718, -0.0044463314, 0.061373208, 0.051597368, -0.064305276, -0.050343633, 0.06579279, -0.08761853, -0.04921584, -0.0031962516, 0.029409816, -0.035726313, 0.015602501, 0.056204304, -0.0020416053, -0.026324106, -0.025729423, 0.104078926, 0.0076009072, 0.018787442, 0.031772655, 0.035729043, 0.022186806, 0.055047274, 0.048344437, 0.015010571, -0.0012024436, -0.050350774, -0.024710411, 0.013609895, -0.009427472, 0.09580724, 0.035913005, 0.055471156, -0.060681727, 0.01639029, 0.022190962, -0.05541275, 0.02252715, 0.031125216, 0.010879646, 0.010300303, -0.018512394, -0.0056330804, 0.02458951, 0.085698545, -0.004816602, -0.034936868, -0.045250848, -0.014376478, 0.03849654, 0.02146781, 0.0228461, 0.03572782, -0.031426143, -0.017756125, 0.023589976, -0.018548708, 0.020143818, -0.0032234285, 0.068655655, 0.05891859, -0.029297994, -0.0444489, 0.003439056, -0.03712702, 0.010371364, -0.014805026, -0.04363112, 0.0044533983, 0.025326489, -0.07153489, 0.048387244, -0.025175577, -0.02407683, -0.06973501, -0.043239526, 0.01657844, -0.014159211, -0.04010814, -0.035094757, -0.07352012, -0.0057208617, 0.034322336, -0.047614865, -0.038756162, 0.019561868, 0.01069496, 0.056435045, -0.024837933, 0.021709671, -0.02181519, 0.007243642, 0.0011034086, 0.013526423, 0.054702245, -0.015464005, 0.052431196, 0.019740466, -0.026860101, 0.05255439, 0.005928022, -0.04875306, -0.00840115, -0.046129934, 0.022203395, 0.0002085332, 0.048062284, 0.031221244, -0.00927902, -0.060726177, -0.0057565537, 0.038432293, 0.042361837, -0.014363057, 0.053103544, 0.023257805, 0.07453622, -0.023251569, -0.004816142, 0.000952417, -0.010476217, 0.0009938043, 0.014692788, 0.00983403, -0.003658156, 0.006930668, 0.060954664, -0.049138602, -0.015449959, -0.08807367, 0.0010196314, 0.071770504, 0.010531853, 0.027007677, -0.022224728, 0.016723424, 0.0014374983, -0.08856743, -0.04354327, 0.052986994, -0.037863407, 0.018218614, -0.096008025, -0.020143239, -0.038959824, 0.0057801637, -0.0043531535, -0.012625324, 0.03320512], limit=1)
    # if search_result:
    #     print(search_result[0].payload['text'])
    # else:
    #     print("No results found or search_result is None")
    encoded = embedding.encode("What is PDPA")
    print(encoded["embeddings"][0])