'use client';

import { useStudentWorkflowContext } from './context/student-workflow';
import { ResearchSection } from './research-section';

export function ProgressSection() {
  const { researchType } = useStudentWorkflowContext();

  return (
    <>
      <div className="prose dark:prose-h1:text-white capitalize">
        <h1>{researchType}</h1>
      </div>

      <ResearchSection />

      {/* <section className="space-y-20 divide-y">
        <div className="pt-10 pb-5 space-y-20">
          <Stepper
            steps={[
              'Proposal',
              'Pre-Oral Defense',
              'Ethics',
              'Full Manuscript',
              'Final Defense',
              'Copyright',
            ]}
            currentStep={0}
            className="justify-center"
          />

          <div className="">
            <article className="prose prose-sm">
              <h2>Full Manuscript</h2>

              <ul>
                <li>
                  <h3>Content</h3>
                  <p>
                    Lorem ipsum dolor sit amet consectetur adipisicing elit.
                    Aperiam deleniti, sit reprehenderit accusantium placeat,
                    animi, atque esse saepe ea nostrum nihil earum quidem
                    laboriosam. Et accusamus dicta reiciendis. Ipsa, natus.
                  </p>
                </li>
                <li>
                  <h3>Abstract</h3>
                  <p>
                    Lorem ipsum dolor sit amet consectetur adipisicing elit.
                    Aperiam deleniti, sit reprehenderit accusantium placeat,
                    animi, atque esse saepe ea nostrum nihil earum quidem
                    laboriosam. Et accusamus dicta reiciendis. Ipsa, natus.
                  </p>
                </li>
              </ul>
            </article>
          </div>
        </div>
      </section> */}
    </>
  );
}
