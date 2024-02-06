'use client';

import { Card, CardContent, CardHeader } from '@/components/ui/card';
import DocViewer, { DocViewerRenderers } from '@cyntler/react-doc-viewer';

export function ResearchManualSection() {
  const docs = [
    {
      uri: 'https://ik.imagekit.io/0x1lnkvjw/PUP_-_University_Thesis_and_Dissertation_Manual_with_ISBN_as_of_08.07.17_RC1dDSLX4.pdf?updatedAt=1699843692653',
    },
  ];

  return (
    <section>
      <Card>
        <CardHeader className="prose max-w-none">
          <h2>PUP Research Manual</h2>
        </CardHeader>
        <CardContent>
          <article className="prose max-w-none mt-5">
            <p>
              The PUP Research Manual encompasses essential information,
              policies, and explanations related to the execution of research
              projects within the University. It offers insights into the
              procedures for submitting research proposals to secure University
              funding, the financial incentives and support available to our
              researchers, and the relevant guidelines and policies governing
              research funding. The manual concludes with a comprehensive
              discussion on the ethical principles that underlie our research
              endeavors as an institution.
            </p>

            <p>
              The PUP Research Manual is a valuable resource intended for use by
              all researchers at the University, including faculty members,
              administrative and non-teaching personnel, and students. It has
              been developed with reference to various local and international
              educational institutions, ensuring alignment with globally
              recognized standards in academic research.
            </p>
          </article>

          <div className="mt-10">
            <DocViewer
              documents={docs}
              pluginRenderers={DocViewerRenderers}
              theme={{
                primary: '#f4f4f4',
                textPrimary: '#000000',
              }}
            />
          </div>
        </CardContent>
      </Card>
    </section>
  );
}
