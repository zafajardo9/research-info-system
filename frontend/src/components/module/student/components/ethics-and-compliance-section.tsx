import { Card, CardContent, CardHeader } from '@/components/ui/card';
import Link from 'next/link';

export function EthicsAndComplianceSection() {
  return (
    <section>
      <Card>
        <CardHeader className="prose max-w-none">
          <h2>Ethics and Compliance</h2>
          <p>
            Welcome to the Ethics and Compliance page of PUP&apos;s Research
            Information System. At PUP, we are committed to upholding the
            highest ethical standards and ensuring compliance with all relevant
            regulations in the pursuit of research excellence. This page serves
            as a central resource to guide researchers, students, and faculty in
            matters of ethical conduct and regulatory compliance.
          </p>
        </CardHeader>
        <CardContent>
          <article className="prose max-w-none mt-5">
            <h3>RMO Centers</h3>

            <ul>
              <li>
                Research Evaluation and Monitoring Center. The REMC monitors the
                implementation of the approved internally and externally funded
                research projects. It also assists in the preparation of program
                designed towards the development of national and international
                relations.
              </li>

              <li>
                Research Support Center. The RSC facilitates the requests for
                research assistance, grants and/or incentives.
              </li>

              <li>
                Center for Research Ethics. The CRE facilitates the requests for
                ethics clearance. The centers ensure to protect potential
                participants in the research, but it must also consider
                potential risks and benefits for the community in which the
                research will be carried out. Its goal is to promote high
                ethical standards in research.
              </li>

              <li>
                Center for Research Dissemination and Linkages. The CRDL
                facilitates the forging of linkages to various institutions that
                will result in external funding of research projects and
                programs and organize/co-organize research-related conferences,
                seminars, trainings, fora, etc. as a research dissemination
                platform.
              </li>
            </ul>

            <h3>Downloads</h3>

            <ul>
              <li>
                <Link href="https://onedrive.live.com/view.aspx?cid=C5FB49234DD366A6&resid=C5FB49234DD366A6%21364&app=WordPdf&authkey=%21AKG-fzo_rLLFggE">
                  Faculty Monograph Pamplet (PDF 308 KB)
                </Link>
              </li>
              <li>
                <Link href="https://onedrive.live.com/view.aspx?cid=C5FB49234DD366A6&resid=C5FB49234DD366A6%21366&app=Word">
                  PUP Research Proposal Guide (MS Word 18 KB)
                </Link>
              </li>
              <li>
                <Link href="https://drive.google.com/file/d/1VAmXSdy2hkA6H76--GZlMjZANOkvr6Vo/view">
                  Research Forms and Memorandum Orders (9 MB) ZIP file
                  containing the following documents:
                </Link>
              </li>
              <li>
                <Link href="#">
                  CAPSULIZED RESEARCH PROPOSAL TEMPLATE, Form 1 ETHICS REVIEW,
                  Form 1 TERMS OF REFERENCE, Form 1.2 ETHIC REVIEW, Form 2 LINE
                  ITEM BUDGET, Form 2 RESEARCH PROTOCOL, Form 3 SCHEDULE OF
                  OUTPUTS.TRANCHE RELEASE, Form 4 WORKPLAN, JOURNAL TEMPLATE,
                  REMC PROGRESS REPORT TEMPLATE, RUBRIC IR Form 1, and RUBRIC IR
                  Form 2
                </Link>
              </li>
              <li>
                <Link href="#">
                  Memorandum Order 04 - implementing guidelines of univ.
                  research ethics board structure and functions
                </Link>
              </li>
              <li>
                <Link href="#">
                  Memorandum Order 10 - IMPLEMENTING GUIDELINES FOR THESIS &
                  DISSERTATION GRANT
                </Link>
              </li>
            </ul>
          </article>
        </CardContent>
      </Card>
    </section>
  );
}
